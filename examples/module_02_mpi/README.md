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
