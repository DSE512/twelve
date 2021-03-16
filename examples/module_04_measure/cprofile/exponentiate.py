def build_list():
    return [x for x in range(1_000_000)]


def exponentiate(arry, power):
    return [x**power for x in arry] 


def main():
    my_list = build_list()
    squared = exponentiate(my_list, 2)


if __name__ == '__main__':
    import cProfile, pstats

    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()   

