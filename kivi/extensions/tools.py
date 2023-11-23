# Author: https://github.com/Itz-fork
# Project: Kivi.py

from functools import wraps
from threading import Thread
from itertools import islice


def run_on_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs).start()
        return

    return wrapper


def slice_dict(dt: dict):
    SIZE = 1000
    it = iter(dt)
    for i in range(0, len(dt), SIZE):
        yield {k: dt[k] for k in islice(it, SIZE)}
