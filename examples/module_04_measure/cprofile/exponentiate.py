import cProfile


def build_list():
    return [x for x in range(1_000)]


def exponentiate(arry, power):
    return [x**power for x in arry]


def main():
    my_list = build_list()
    squared = exponentiate(my_list, 2)


if __name__ == '__main__':
    cProfile.run('main()')

