# MinIO Integration With ClickHouse

The `docker-compose` environment to test MinIO Integration with ClickHouse.

## Prerequisites

You must have the following installed on your system.

* [git]
* [docker]
* [docker-compose]

## Services

The following services are provided by the `docker-compose` cluster.

* `clickhouse1` - ClickHouse node 1
* `clickhouse2` - ClickHouse node 2
* `clickhouse3` - ClickHouse node 3
* `zookeeper` - Zookeeper node
* `minio` - MinIO node

## How To Run

Clone this repository and enter `docker-compose` folder.

```bash
cd docker-compose/
```

```bash
docker-compose up -d
```
