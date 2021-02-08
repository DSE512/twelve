<h1 align="center">MPI Examples<span></span></h1>

# hello.py

Print hello and the communicator size from each MPI rank.

```
mpirun -n 4 python hello.py
```


# broadcast.py

Broadcast a random numpy array from one rank to all ranks.

```
mpirun -n 4 python broadcast.py
```

# scatter_gather.py

Scatter a list to all of the workers and gather it back to rank 0.

```
mpirun -n 3 python scatter_gather.py
```

# all_gather.py

Scatter a list to all of the workers and gather those values to all ranks.

```
mpirun -n 3 python all_gather.py
```

# reduce.py

Scatter a list to all of the workers and reduce those values to `rank 0`. Note that
I am switching up the values that are being scattered compared with `scatter_gather.py`.

```
mpirun -n 3 python reduce.py
```

# all_reduce.py

Scatter a list to all of the workers and reduce those values on `all ranks`. Note that
I am switching up the values that are being scattered compared with `scatter_gather.py`.

```
mpirun -n 3 python allreduce.py
```
