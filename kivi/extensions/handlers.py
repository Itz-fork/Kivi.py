# Author: https://github.com/Itz-fork
# Project: Kivi.py

from functools import wraps
from inspect import cleandoc
from threading import Thread
from json.decoder import JSONDecodeError

from kivi.erros import KV_NODATA


def handle_erros(func):
    @wraps(func)
    def hwrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            print(
                cleandoc(
                    f"""
            Raised by: {func.__name__} | IndexError
            Reason: Occurs when you're trying to access a database without loading it to the memory
            Can be fixed by:
                # Load ddatabase to the memory
                data = dict or path to the database
                db.kv_load(data)
            """
                )
            )

        except KeyError:
            # Return a empty list for queries
            if func.__name__ == "kv_query":
                return []
            # Otherwise show an error
            print(
                cleandoc(
                    f"""
            Raised by: {func.__name__} | KeyError
            Reason: Occurs when data is not in correct format
            Can be fixed by:
                # If you're reading/setting/loading data
                    # Format data to kivi standard format
                    x = db._kv_format(data)
                    y = db.kv_load(x)
                
                # If you're running a query
                    # Index the query using kv_index
                    db.kv_index(data, ["fields", "to", "index"])
            """
                )
            )

        except KV_NODATA:
            print(
                cleandoc(
                    f"""
            Raised by: {func.__name__}
            Reason: KV_NODATA is called when you're trying to create/save to database without giving data to do so
            """
                )
            )

        except JSONDecodeError:
            print(
                cleandoc(
                    f"""
            Raised by: {func.__name__} | JSONDecodeError
            Reason:
                Occurs when trying to load a database with incorrect json format.
                Usually happens when you try to load a database right after creating it
            Can be fixed by:
                # Wait till the database is saved to fs
                db.kv_create("wow", data)
                sleep(2)
                db.kv_load("/home/test/data/previous.json")
            """
                )
            )

        except Exception as e:
            print(
                cleandoc(
                    f"""
            Raised by: {func.__name__} | UnknownException
            Reason:
                {e}
            """
                )
            )
        return

    return hwrapper


def run_on_thread(func):
    @wraps(func)
    def rot_wrapper(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs).start()
        return

    return rot_wrapper
