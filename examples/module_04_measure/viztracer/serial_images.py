from twelve.data import Images
from viztracer import VizTracer


def main():
    tracer = VizTracer()
    tracer.start()

    images = Images("img")

    tracer.stop()
    tracer.save("viztrace_results.html")


if __name__=="__main__":
    main()
