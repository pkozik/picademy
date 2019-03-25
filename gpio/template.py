
from time import sleep

def go():
    for ix in range(10):
        print "iteration: %d" % ix
        sleep(0.5)


if __name__ == "__main__":
    try:
        go()

    except KeyboardInterrupt:
        exit(0)
