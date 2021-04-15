# Pipeline Parallelism with RPC

A convolutional model is divided into two shards and the input batch 
is partitioned into multiple splits and fed into the two model shards 
in a pipelined fashion. Instead of parallelizing the execution using 
CUDA streams, we will useasynchronous RPCs. This will work across 
machine boundaries.
