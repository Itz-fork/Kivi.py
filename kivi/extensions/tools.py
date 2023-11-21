# Author: Itz-fork
# Project: Kivi.py

from threading import Thread
from functools import wraps


def run_on_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs).start()
        return
    return wrapper