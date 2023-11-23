# Author: https://github.com/Itz-fork
# Project: Kivi.py

class KV_NODATA(Exception):
    def __init__(self, e=""):
        super().__init__(
            f"""Unable to execute the function as there aren't enough data. {'raised from ' + e if e else ''}"""
        )
