def gustafsons_law(num_proc, a_seq):
    """Gustafson-Barsis law for data parallelism

    Gustafson-Barsis' Law states that the optimal
    speedup is asymptotically `speedup(P) = P * \alpha_{par}`.
    When the problem size increases for a fixed serial 
    problem, our speedup grows as more processors are added.

    Args:
        num_proc: number of processors
        a_seq: proportion of sequential steps in the algorithm
    """
    return num_proc - a_seq * (num_proc-1)
