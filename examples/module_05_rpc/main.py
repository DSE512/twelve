import os
import time
import threading

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.multiprocessing as mp

import torch.distributed.rpc as rpc
from torch.distributed.rpc import RRef
import torch.distributed.autograd as dist_autograd
from torch.distributed.optim import DistributedOptimizer


image_w = 28
image_h = 28
num_batches = 3
num_classes = 10
batch_size = 120


class BaseRPC(nn.Module):
    """Base module to get RRefs"""

    def __init__(self):
        super(BaseRPC, self).__init__()
        self._lock = threading.Lock()

    def parameter_rrefs(self):
        return [RRef(p) for p in self.parameters()]


class ConvShard(BaseRPC):
    """The early part of our network - convolutions"""

    def __init__(self, device):
        super(ConvShard, self).__init__()

        self.device = device

        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 3, 1),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, 1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        ).to(device)

    def forward(self, x_rref):
        x = x_rref.to_here().to(self.device)

        with self._lock:
            out = self.conv(x)

        return out.cpu()


class ClassifierShard(BaseRPC):
    """Second half of our network - classifier"""

    def __init__(self, device):
        super(ClassifierShard, self).__init__()

        self.device = device

        self.classifier = nn.Sequential(
            nn.Linear(9216, 128),
            nn.ReLU(),
            nn.Linear(128, 10),
            nn.LogSoftmax(dim=1)
        ).to(device)

    def forward(self, x_rref):
        x = x_rref.to_here().to(self.device)
        x = torch.flatten(x, 1)

        with self._lock:
            out = self.classifier(x)

        return out.cpu()


class DistCNN(nn.Module):
    """Combine the two shards of our model"""

    def __init__(self, split_size, workers):
        super().__init__()

        self.split_size = split_size

        self.p1_rref = rpc.remote(
            workers[0],
            ConvShard,
            args = ("cuda:0",)
        )

        self.p2_rref = rpc.remote(
            workers[1],
            ClassifierShard,
            args = ("cuda:1",)
        )

    def forward(self, xs):
        out_futures = []
        for x in iter(xs.split(self.split_size, dim=0)):
            x_rref = RRef(x)
            y_rref = self.p1_rref.remote().forward(x_rref)
            z_fut = self.p2_rref.rpc_async().forward(y_rref)
            out_futures.append(z_fut)

        # collect and cat all output tensors into one tensor.
        return torch.cat(torch.futures.wait_all(out_futures))

    def parameter_rrefs(self):
        remote_params = []
        remote_params.extend(
            self.p1_rref.remote().parameter_rrefs().to_here()
        )
        remote_params.extend(
            self.p2_rref.remote().parameter_rrefs().to_here()
        )
        return remote_params


def run_main_process(split_size):
    # put the two model parts on worker1 and worker2 respectively
    model = DistCNN(split_size, ["worker1", "worker2"])

    loss_fn = nn.MSELoss()

    opt = DistributedOptimizer(
        optim.SGD,
        model.parameter_rrefs(),
        lr=0.05,
    )

    one_hot_indices = torch.LongTensor(batch_size) \
                           .random_(0, num_classes) \
                           .view(batch_size, 1)

    for i in range(num_batches):
        print(f"Processing batch {i}")
        # generate random inputs and labels
        inputs = torch.randn(batch_size, 1, image_w, image_h)
        labels = torch.zeros(batch_size, num_classes) \
                      .scatter_(1, one_hot_indices, 1)

        # The distributed autograd context is the dedicated scope for the
        # distributed backward pass to store gradients, which can later be
        # retrieved using the context_id by the distributed optimizer.
        with dist_autograd.context() as context_id:
            outputs = model(inputs)

            dist_autograd.backward(
                context_id,
                [loss_fn(outputs, labels)]
            )

            opt.step(context_id)


def run_worker(rank, world_size, num_split):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '29500'

    options = rpc.TensorPipeRpcBackendOptions(
         num_worker_threads=256, rpc_timeout=300
    )

    if rank == 0:
        rpc.init_rpc(
            "main_process",
            rank=rank,
            world_size=world_size,
            rpc_backend_options=options
        )
        run_main_process(num_split)
    else:
        rpc.init_rpc(
            f"worker{rank}",
            rank=rank,
            world_size=world_size,
            rpc_backend_options=options
        )
        pass

    # block until all rpcs finish
    rpc.shutdown()


if __name__=="__main__":
    world_size = 3
    for num_split in [1, 2, 4, 8]:
        tik = time.perf_counter()

        mp.spawn(
            run_worker,
            args=(world_size, num_split),
            nprocs=world_size,
            join=True
        )

        tok = time.perf_counter()

        print(f"number of splits = {num_split}, execution time = {tok - tik}")

