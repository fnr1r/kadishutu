import traceback
import sys


def printf(txt: str, *args, **kwargs):
    print(txt.format(*args), **kwargs)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def eprintf(txt: str, *args, **kwargs):
    print(txt.format(*args), file=sys.stderr, **kwargs)


def printexcept(msg: str, e: Exception, *args: object, **kwargs: object):
    eprint(
        msg.format(*args, **kwargs) + ": (traceback below)\n",
        "".join(traceback.format_exception(e)),
        sep="",
    )
