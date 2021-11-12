DROP DATABASE IF EXISTS finCube;

CREATE DATABASE IF NOT EXISTS finCube;

DROP TABLE IF EXISTS finCube.factTable;

CREATE TABLE IF NOT EXISTS finCube.factTable (`index` Int64, `int0` Int64, `int1` Int64, `int2` Int64, `int3` Int64, `int4` Int64, `int5` Int64, `int6` Int64, `int7` Int64, `int8` Int64, `int9` Int64, `int10` Int64, `int11` Int64, `int12` Int64, `int13` Int64, `int14` Int64, `int15` Int64, `int16` Int64, `int17` Int64, `int18` Int64, `int19` Int64, `int20` Int64, `int21` Int64, `int22` Int64, `int23` Int64, `int24` Int64, `int25` Int64, `int26` Int64, `int27` Int64, `int28` Int64, `int29` Int64, `int30` Int64, `int31` Int64, `int32` Int64, `int33` Int64, `dttime0` Datetime, `dttime1` Datetime, `dttime2` Datetime, `dttime3` Datetime, `dttime4` Datetime, `dttime5` Datetime, `dttime6` Datetime, `dttime7` Datetime, `dttime8` Datetime, `dttime9` Datetime, `dttime10` Datetime, `dttime11` Datetime, `dttime12` Datetime, `dttime13` Datetime, `dttime14` Datetime, `dttime15` Datetime, `dttime16` Datetime, `dttime17` Datetime, `dttime18` Datetime, `dttime19` Datetime, `dttime20` Datetime, `dttime21` Datetime, `dttime22` Datetime, `dttime23` Datetime, `dttime24` Datetime, `dttime25` Datetime, `dttime26` Datetime, `dttime27` Datetime, `dttime28` Datetime, `dttime29` Datetime, `dttime30` Datetime, `dttime31` Datetime, `dttime32` Datetime, `str0` String, `str1` String, `str2` String, `str3` String, `str4` String, `str5` String, `str6` String, `str7` String, `str8` String, `str9` String, `str10` String, `str11` String, `str12` String, `str13` String, `str14` String, `str15` String, `str16` String, `str17` String, `str18` String, `str19` String, `str20` String, `str21` String, `str22` String, `str23` String, `str24` String, `str25` String, `str26` String, `str27` String, `str28` String, `str29` String, `str30` String, `str31` String, `str32` String, `arrFloat` Array(Float), `partition` Int64) ENGINE = MergeTree() PARTITION BY partition ORDER BY tuple() SETTINGS index_granularity = 8192;

CREATE TABLE finCube.factTable_all AS finCube.factTable
ENGINE = Distributed(sharded_cluster, finCube, factTable, rand());

/* cat script.sql | clickhouse-client -mn */