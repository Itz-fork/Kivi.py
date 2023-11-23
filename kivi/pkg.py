# Author: https://github.com/Itz-fork
# Project: Kivi.py

import json, re, sys
from os import path, getcwd, mkdir

from kivi.extensions.converter import data_conv
from kivi.extensions.tools import run_on_thread, slice_dict

from kivi.erros import KV_NODATA

# sys.


class Kivi(object):
    """
    Kivi database
    """

    KV_DB = []
    kv_src = f"{getcwd()}/.kivi_db"

    def __init__(self, src: str = None, to_load: list = []):
        if src:
            self.kv_src = src
        # Create databse path if it doesn't exist
        if not path.isdir(self.kv_src):
            mkdir(self.kv_src)
        # Load databases
        if to_load:
            for db in to_load:
                self.kv_load(db)

    def kv_create(self, name: str, data: dict):
        """
        Creates a new database and load it to the memory

        Arguments:
            name: Name of the database
            data: Dict consist of data

        Example:
            ```py
            db.kv_create("wow", {"user-1": 123456})
            ```
        """
        _tmpdb = {"name": name}
        _tmpdb["items"] = self._kv_format(data)
        self._kv_save(data=_tmpdb)

    def kv_load(self, data: dict | str) -> int:
        """
        Loads database into the memory

        Arguments:
            data: Path to a json file or python dict

        Returns:
            Index of the database

        Example:
            ```py
            db.kv_load("/home/test/data/stuff.json")
            ```
        """
        kvdt = {}
        if isinstance(data, str):
            if not path.isfile(data):
                raise FileNotFoundError(f"File {data} does not exists")
            with open(data, "rb") as kvf:
                kvdt = json.load(kvf)
        else:
            kvdt = data
        self.KV_DB.append(kvdt)
        return len(self.KV_DB) - 1

    def kv_get(self, index: int, key: str):
        """
        Get key from a database

        Arguments:
            index: Index of the database (returned in kv_load or when creating the instance)
            key: Key!

        Example:
            ```py
            db.kv_get(0, "greeting")
            ```
        """
        try:
            frm_db = self.KV_DB[index]["items"][key]
            return data_conv(frm_db[0], frm_db[1])
        except KeyError as e:
            raise KeyError(f"Value doesn't exists in database at index {index}") from e

    def kv_merge(self, index: int, tomerge: dict, to_std: bool = True):
        """
        Merge data into the database

        Arguments:
            index: Index of the database (returned in kv_load or when creating the instance)
            tomerge: Dict consist of data that needs to be merged

        Note:
            If the tomerge dict is not in the kivi formatting, set to_std = True

        Example:
            ```py
            dt = {
                "thing-1": [123, True, {'user1': 'gibberish?#45'}],
                "thing-2": [123, True, {'user2': 'gibberish?#45', 'nuh': True}]
            }
            db.kv_merge(index=0, tomerge=dt, to_std=True)
            ```
        """
        _svdb = self.KV_DB[index]["items"]
        if to_std:
            tomerge = self._kv_format(tomerge)
        self.KV_DB[index]["items"] = {**_svdb, **tomerge}
        self._kv_save(index=index)

    def kv_set(self, index: int, key: str, data):
        """
        Add key to a database

        Arguments:
            index: Index of the database (returned in kv_load or when creating the instance)
            key: Key!

        Example:
            ```py
            db.kv_set(0, "gtr1", "greeting")
            ```
        """
        try:
            self.KV_DB[index]["items"][key] = [str(data), type(data).__name__]
            # Save the file
            self._kv_save(index=index)
            return index
        except KeyError as e:
            raise KeyError(f"Value doesn't exists in database at index {index}") from e
        except IndexError as e:
            raise IndexError(
                f"{e} \n\nPerhaps you forgot to run `db.kv_load(path)` ?"
            ) from e

    def kv_search(self, index: int, query: str, strict: bool = True):
        """
        Search for string in a database

        Arguments:
            index: Index of the database (returned in kv_load or when creating the instance)
            query: String to re.search for in the database
            strict: Pass 'False' to get more results

        Example:
            ```py
            db.kv_search(0, "Spider man")
            ```
        """
        _tdb = self.KV_DB[index]["items"]
        _sfnc = re.match if strict else re.search
        qry = query.split(" ")
        rgx = (
            r"(?i)([+" + qry.pop(0) + "]+\s)" + "".join(f"|(\b[+{i}]+\s)" for i in qry)
            if len(qry) > 1
            else f"(?i)([+{query}]+\s)"
        )
        return list(
            filter(
                str.strip,
                map(
                    lambda i: {i[0]: i[1][0]} if _sfnc(rgx, i[1][0]) else "",
                    _tdb["items"].items(),
                ),
            )
        )

    def kv_query(self, index: int, query: str, chars: int = 3):
        """
        WIP

        Search for string in an indexed database

        Arguments:
            index: Index of the database (returned in kv_load or when creating the instance)
            query: String to search for in the database
            chars: Set this to the value you used when indexing data

        Example:
            ```py
            db.kv_query(0, "Spider man")
            ```
        """
        query = query.lower()
        _tdb = self.KV_DB[index]
        qry = query.split(" ")
        results = []
        for q in qry:
            _tlist = _tdb[q[:chars]]
            rgx = rf"(?i)([+{q}])"
            while _tlist:
                itm = _tlist.pop()
                if re.match(rgx, itm["searchable"]) and itm["origin"] not in results:
                    results.append(itm["origin"])
        return results

    def kv_index(self, data: dict | list, fields: list, chars: int = 3):
        """
        Index data to perform queries much faster

        Arguments:
            data: Data to index (a dict or list of dicts)
            fields: Json fields that needs to be indexed
            chars: Amount of characters that indexed key can have (Ex: "Spider" will be sliced to "spi" to create the key for index)

        Example:
            ```py
            data = [
                {"title": "Spooder man", "extract": "Marvel spooder man!"},
                {"title": "Iron deficiency man", "extract": "Marvel no Fe?"}
            ]
            db.kv_index(data, ["title", "extract"], 3)
            ```
        """
        print(
            f"Items to index: {len(data)}\nIndexing started. This may take a while..."
        )
        _tmal = {}

        # search for fields and creates a index
        def index_from_fields(sdt):
            for k, v in sdt.items():
                if isinstance(v, dict):
                    return index_from_fields(v)
                if k in fields:
                    _lvrs = [re.sub("\W+", "", _spl) for _spl in str(v).split(" ")]
                    for _tv in _lvrs:
                        if not _tv:
                            pass
                        _vchr = str(_tv)[:chars].lower()
                        _rs = _tmal.get(_vchr)
                        if _rs:
                            _rs.append({"searchable": _tv, "origin": {k: v}})
                        else:
                            _tmal[_vchr] = [{"searchable": _tv, "origin": {k: v}}]

        if isinstance(data, list):
            for di in data:
                index_from_fields(di)
        else:
            index_from_fields(data)
        print("Indexing finished")
        self._kv_save(name="movie_indexed", data=_tmal)

    def _kv_format(self, data: dict) -> dict:
        return dict(
            map(
                lambda i: (i[0], [str(i[1]), type(i[1]).__name__]),
                data.items(),
            )
        )

    @run_on_thread
    def _kv_save(self, name: str = None, index: int = None, data: dict = None):
        """
        Save the database into a json file

        Arguments:
            index: Index of the database (returned in kv_load or when creating the instance)
            data: Dict consist of data in kivi.py format
        """
        _svdb = data if data else self.KV_DB[index] if isinstance(index, int) else {}
        if _svdb:
            _jpth = f"{self.kv_src}/{name if name else _svdb['name']}.json"
            with open(_jpth, "w", encoding="utf-8") as tosav:
                json.dump(_svdb, tosav, indent=4, ensure_ascii=False)
                # tosav.truncate()
        else:
            raise KV_NODATA("_kv_save: Used to save the database into a json file")
