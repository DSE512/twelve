from monte import monte_carlo_pi


def main():
    pi = monte_carlo_pi(num_iterations=100_000_000)
    print(f"Approximation of pi: {pi:.5f}")


if __name__=="__main__":
    from viztracer import VizTracer

    tracer = VizTracer()
    tracer.start()

    main()

    tracer.stop()
    tracer.save("results.html")
