import re
from dataclasses import dataclass
import string
import random
from time import time
import numpy as np
import pandas as pd


class FactGenerator:
    def __init__(self, arr_length, nb_rows, nb_part):
        self.fdf = FactDataFrame(arr_length, nb_rows, nb_part)

    def get_fact_stream(self):
        for entry in self.fdf.create():
            yield entry


class FactDataFrame:
    def __init__(self, arr_length, nb_rows, nb_part):
        self._arr_length = arr_length
        self._nb_rows = nb_rows
        self._nb_part = nb_part
        self.nb_cats = min(int(nb_rows ** 0.5), 100)
        self.max_int = 10 ** 6
        self.date_min = pd.to_datetime("2018-01-01")
        self.date_max = pd.to_datetime("2050-12-31")
        self.table_spec = dict(
            **{f"int{i}": "int" for i in range(34)},
            **{f"dttime{i}": "datetime" for i in range(33)},
            **{f"str{i}": "str" for i in range(33)},
        )

    def create(self):
        myrnd = random.Random(0)
        np.random.seed(0)
        myrnd.seed(0)

        cats = {
            # Generate a list of nb_cats random-sized strings built from random letters & digits
            "str": [
                "".join(myrnd.choice(string.ascii_letters) for _ in range(x))
                for x in np.random.randint(5, 20, size=self.nb_cats)
            ],
            # Generate a list of nb_cats random int64s
            "int": np.random.randint(-self.max_int, self.max_int, size=self.nb_cats, dtype=np.int64),
            # Generate a list of nb_cats random DateTimes
            "datetime": (
                np.random.randint(
                    self.date_min.value // 10 ** 9,
                    self.date_max.value // 10 ** 9,
                    size=self.nb_cats,
                    dtype=np.int64,
                )
            )
            * 10 ** 9,
        }

        result = pd.DataFrame(
            {
                name: (
                    np.random.choice(cats[typ], size=self._nb_rows)
                    if typ in ["str", "int"]
                    else np.random.choice(cats[typ], size=self._nb_rows).view("M8[ns]")
                    if typ == "datetime"
                    else np.nan
                )
                for name, typ in self.table_spec.items()
            }
        ).reset_index()

        if self._arr_length > 0:
            result["arrFloat"] = list(np.random.rand(self._nb_rows, self._arr_length) * 1e6)
        
        result["partition"] = np.random.randint(self._nb_part)

        return result
