# Author: https://github.com/Itz-fork
# Project: Kivi.py


from itertools import islice


def slice_dict(dt: dict, size: int):
    it = iter(dt)
    for i in range(0, len(dt), size):
        yield {k: dt[k] for k in islice(it, size)}
