def amdahls_law(p, s):
    """Speedup relative to proportion parallel

    Amdahl's Law gives an idealized speedup we 
    can expect for an algorithm given the proportion
    that algorithm can be parallelized and the speed
    we gain from that parallelization. The best case
    scenario is that the speedup, `s`, is equal to
    the number of processors available.

    Args:
        p: proportion parallel
        s: speed up for the parallelized proportion
    """
    return 1 / ((1-p) + p/s)
