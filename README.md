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

```bash
Creating network "docker-compose_default" with the default driver
Creating docker-compose_zookeeper_1 ... done
Creating docker-compose_minio_1     ... done
Creating docker-compose_minio-client_1 ... done
Creating docker-compose_clickhouse1_1  ... done
Creating docker-compose_clickhouse3_1  ... done
Creating docker-compose_clickhouse2_1  ... done
Creating docker-compose_all_services_ready_1 ... done
```

> Note: You must run all `docker-compose` commands inside the `docker-compose` folder.

Check that all services are up and healthy.

 ```bash
docker-compose ps
```

```bash
               Name                              Command                  State                    Ports              
----------------------------------------------------------------------------------------------------------------------
docker-compose_all_services_ready_1   /hello                           Exit 0                                         
docker-compose_clickhouse1_1          bash -c clickhouse server  ...   Up (healthy)   8123/tcp, 9000/tcp, 9009/tcp    
docker-compose_clickhouse2_1          bash -c clickhouse server  ...   Up (healthy)   8123/tcp, 9000/tcp, 9009/tcp    
docker-compose_clickhouse3_1          bash -c clickhouse server  ...   Up (healthy)   8123/tcp, 9000/tcp, 9009/tcp    
docker-compose_minio-client_1         /bin/sh -c  /usr/bin/mc co ...   Exit 0                                         
docker-compose_minio_1                /usr/bin/docker-entrypoint ...   Up (healthy)   9000/tcp, 0.0.0.0:9001->9001/tcp
docker-compose_zookeeper_1            /docker-entrypoint.sh zkSe ...   Up (healthy)   2181/tcp, 2888/tcp, 3888/tcp    
```

### Working With Services

### ClickHouse Nodes

```bash
docker-compose exec clickhouse1 bash -c 'clickhouse-client -q "SELECT version()"'
```

```bash
docker-compose exec clickhouse2 bash -c 'clickhouse-client -q "SELECT version()"'
```

```bash
docker-compose exec clickhouse3 bash -c 'clickhouse-client -q "SELECT version()"'
```

[git]: https://git-scm.com/
[docker]: https://www.docker.com/
[docker-compose]: https://docs.docker.com/compose/
