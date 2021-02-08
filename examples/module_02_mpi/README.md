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
