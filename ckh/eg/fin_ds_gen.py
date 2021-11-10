import os
import string
import random
from time import time
import numpy as np
import pandas as pd
from clickhouse_driver import Client

# ClickHouse Ops
host = os.environ.get("CLICKHOUSE_HOST", "localhost")
port = os.environ.get("CLICKHOUSE_PORT", 9000)
user = os.environ.get("CLICKHOUSE_USER", "default")
pswd = os.environ.get("CLICKHOUSE_PASSWORD", "")

client = Client(host=host, port=port, database="default", user=user, password=pswd)


def convert_type(col_type, value):
    """Convert pandas type to Clickhouse type column"""
    if col_type.name[:3] == "int":
        return f"{col_type.name.capitalize()}"
    elif col_type.name[:8] == "datetime":
        return "Datetime"
    elif col_type.name == "object" and hasattr(value, "__iter__"):
        if isinstance(value, str):
            return "String"
        else:
            return "Array(Float)"
    elif col_type.name == "category" or col_type.name == "object":
        return "String"
    else:
        raise TypeError(f"{col_type.name} not recognize")


def convert_type_ps(col_type, value):
    """Convert pandas type to PostGreSQL type column"""
    if col_type.name[:3] == "int":
        return f"BIGINT"
    elif col_type.name[:8] == "datetime":
        return "timestamp"
    elif col_type.name[:5] == "float":
        return "float8"
    elif col_type.name == "object" and hasattr(value, "__iter__"):
        if isinstance(value, str):
            return "varchar(20)"
        else:
            return "float8"
    elif col_type.name == "category" or col_type.name == "object":
        return "varchar(20)"
    else:
        raise TypeError(f"{col_type.name} not recognize")


t9 = time()
# length of array in arrFloat column
arr_length = int(os.environ.get("ARRAY_LENGTH", 10))
# number of rows in the partition 0
nb_rows = int(os.environ.get("NB_ROWS", 10_000))
# number of partition :
# each partition is copied and modified from the previous tableset and appended to it
# max number of copied rows is 200_000
nb_part = int(os.environ.get("NB_PART", 10))

# number of distinct values in each data type
nb_cats = min(int(nb_rows ** 0.5), 100)
shuffle_cols = False

# Generate Dataframe
nb_cols_int, nb_cols_date, nb_cols_str = 34, 33, 33
table_spec = dict(
    **{f"int{i}": "int" for i in range(nb_cols_int)},
    **{f"dttime{i}": "datetime" for i in range(nb_cols_date)},
    **{f"str{i}": "str" for i in range(nb_cols_str)},
)

# Generate first partition of data (partition=0) in Dafaframe, without array column
myrnd = random.Random(0)
np.random.seed(0)
myrnd.seed(0)
t0 = time()
print(
    f" --> Dataframe generation with {nb_rows:,d} rows x {len(table_spec)} cols and {'no ' if arr_length==0 else f'a {arr_length}-'}array col ... ",
    end="",
)
max_int = 10 ** 6
date_min = pd.to_datetime("2018-01-01")
date_max = pd.to_datetime("2050-12-31")


# Create categorical values for each data type ie. decoration or attributes
chars = string.ascii_letters
cats = {
    # Generate a list of nb_cats random-sized strings built from random letters & digits
    "str": [
        "".join(myrnd.choice(chars) for _ in range(x))
        for x in np.random.randint(5, 20, size=nb_cats)
    ],
    # Generate a list of nb_cats random int64s
    "int": np.random.randint(-max_int, max_int, size=nb_cats, dtype=np.int64),
    # Generate a list of nb_cats random DateTimes
    "datetime": (
        np.random.randint(
            date_min.value // 10 ** 9,
            date_max.value // 10 ** 9,
            size=nb_cats,
            dtype=np.int64,
        )
    )
    * 10 ** 9,
}
# Generate data
result = pd.DataFrame(
    {
        name: (
            np.random.choice(cats[typ], size=nb_rows)
            if typ in ["str", "int"]
            else np.random.choice(cats[typ], size=nb_rows).view("M8[ns]")
            if typ == "datetime"
            else np.nan
        )
        for name, typ in table_spec.items()
    }
).reset_index()

if arr_length > 0:
    result["arrFloat"] = list(np.random.rand(nb_rows, arr_length) * 1e6)

# Add a partition column
result["partition"] = 0
t1 = time()
print(f" --> done in {t1-t0:.2f} sec")
print(f" --> Memory used = {result.memory_usage(deep=True).sum()/1e6:,.1f} MBytes")
t0 = t1

# Drop and (re) create table in Clickhouse
client.execute(f"DROP TABLE IF EXISTS factTable")
flds_spec_ckh = [
    f"`{col}` {convert_type(col_type= typ, value= result[col].iloc[0])}"
    for col, typ in result.dtypes.iteritems()
]
create_table_ckh = (
    f"CREATE TABLE IF NOT EXISTS factTable ({', '.join(flds_spec_ckh)}) "
    "ENGINE = MergeTree() PARTITION BY partition ORDER BY tuple() "
    "SETTINGS index_granularity = 8192"
)
client.execute(create_table_ckh)

# export create table statement in POSTGRESQL
flds_spec_ps = [
    f"`{col}` {convert_type_ps(col_type= typ, value= result[col].iloc[0])}"
    for col, typ in result.dtypes.iteritems()
]
create_table_ps = f"CREATE TABLE IF NOT EXISTS factTable ({', '.join(flds_spec_ps)})"
with open("create_table_ps.sql", "w") as f:
    f.write(create_table_ps)

# Insert into
print(f"INSERT INTO TABLE factTable ... ", end="")
t0 = time()
client.execute(
    "INSERT INTO TABLE factTable VALUES", list(result.itertuples(index=False))
)
print(f"done  in {time()-t0:.2f} sec\n")

# sql expressions to modigy some data
sql_flds = dict(zip(result.columns, result.columns))
sql_flds.update(
    {
        "int0": "int0 + rand() % 10000 - 5000 as int0",
        "int1": "int1 + rand() % 10000 - 5000 as int1",
        "int2": "int2 + rand() % 10000 - 5000 as int2",
        "dttime0": "dttime0 + rand() % 1000000 - 500000 as dttime0",
        "dttime1": "dttime1 + rand() % 1000000 - 500000 as dttime1",
        "dttime2": "dttime2 + rand() % 1000000 - 500000 as dttime2",
    }
)
# Create several partitions by copying existing dataset
for part in range(1, nb_part):
    nextIndex = client.execute("select max(index) from factTable")[0][0] + 1
    sql_flds.update(
        {"index": f"index + {nextIndex} as index", "partition": f"{part} as partition"}
    )

    t0 = time()
    client.execute(
        f"INSERT INTO TABLE factTable ({','.join(sql_flds.keys())}) SELECT {','.join(sql_flds.values())} FROM factTable WHERE index < {nextIndex} + 200000"
    )
    print(
        f"Self copy to partition {part}, from {nextIndex:,d} to {client.execute('select count() from factTable')[0][0]:,d} rows in {time()-t0:.3f} secs."
    )

print(f"\nData generated and inserted in total {time()-t9:.1f} secs.")


# create table with array unfolded
# create table factred as factTable
# alter table factred modify column arrFloat float
# insert into factred select * from factTable ARRAY JOIN arrFloat as arrFloat WHERE index < 2
