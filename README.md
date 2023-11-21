# Kivi.py 🥝
A simple toy key-value database that uses [JSON](https://www.json.org/json-en.html) to store data

## Supported data types

- String
- Boolean
- Integer
- Float
- Lists
- Dict
- Datetime

## Why?
I just wanted a simple database to play around, why everything is so complex

<img src="assests/crying.jpg" width=200, height=auto />


## How it works
Data is stored inside json files in the following format

```json
{
    "name": "lot",
    "items": {...}
}
```

`items` contains the inserted data as a string alongside it's original data type like this,
```json
{
    "name": "lot",
    "items": {
        "thing-1": [
            "{'user': 'gibberish?#45'}",
            "dict"
        ],
        "thing-2": [
            "{'user': 'gibberish?#45'}",
            "dict"
        ]
    }
}
```

When you request data using `kv_get` function, data will be automatically converted back to it's original type ([limitations](#limitations))


## Usage


##### Initialize database
```py
from kivi import Kivi

db = Kivi(
    src="Where the database files should be stored. Defaults to `os.getcwd()/.kivi_db`",
    to_load=["path/to/file.json"])
```

> [!NOTE]
> `to_load` only takes json file with default kivi format.
> If you want to store regular json data use [create](#create) or [merge](#merge)

##### Create
Creates a new database and load it to the memory

- Arguments:
    - `name`: Name of the database
    - `data`: Dict consist of data

- Example:
    ```py
    db.kv_create("wow", {"user-1": 123456})
    ```

##### Get
Get value from a database

- Arguments:
    - `index`: Index of the database (returned in kv_load or when creating the instance)
    - `key`: Key!

- Example:
    ```py
    db.kv_get(0, "greeting")
    ```

##### Set / Update
Add or update key in a database

- Arguments:
    - `index`: Index of the database (returned in kv_load or when creating the instance)
    - `key`: Key!

- Example:
    ```py
    db.kv_set(0, "gtr1", "greeting")
    ```

##### Merge
Merge data into the database

- Arguments:
    - index: Index of the database (returned in kv_load or when creating the instance)
    - tomerge: Dict consist of data that needs to be merged

- Example:
    ```py
    dt = {
        "thing-1": [123, True, {'user1': 'gibberish?#45'}],
        "thing-2": [123, True, {'user2': 'gibberish?#45', 'nuh': True}]
    }
    db.kv_merge(index=0, tomerge=dt, to_std=True)
    ```

> [!Note]
> If the `tomerge` dict is not in the kivi formatting, set `to_std = True`

##### Load
Loads database into the memory

- Arguments:
    - data: Path to a json file or python dict
        
- Returns:
    Index of the database

- Example:
    ```py
    db.kv_load("/home/test/data/stuff.json")
    ```

## Requirements

- Python 3.5+
    - [dependecies](requirements.txt)


### Limitations
The data convertion has lots of limits as of now (I don't plan of updating this either).

For example:

- Complex json structures will fail to convert