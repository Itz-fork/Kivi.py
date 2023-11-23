# Author: https://github.com/Itz-fork
# Project: Kivi.py

from json import loads
from ast import literal_eval
from dateutil.parser import parse


def data_conv(stringfy: str, dtype: str):
    """
    Convert saved data into it's original state
    """
    # Integer
    if "int" in dtype:
        return int(stringfy)
    # Floating point
    elif "float" in dtype:
        return float(stringfy)
    # Boolean
    elif "bool" in dtype:
        return {"True": True, "true": True, "False": False, "false": False}.get(
            stringfy
        )
    # Dictionary
    elif "dict" in dtype:
        return loads(stringfy.replace("'", '"'))
    # List
    elif "list" in dtype:
        return literal_eval(stringfy)
    # Datetime
    elif "datetime" in dtype:
        return parse(stringfy)
    else:
        return stringfy