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
* `minio-client` - MinIO client node

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
docker-compose_minio-client_1         /bin/sh -c  /usr/bin/mc co ...   Up (healthy)                                   
docker-compose_minio_1                /usr/bin/docker-entrypoint ...   Up (healthy)   9000/tcp, 0.0.0.0:9001->9001/tcp
docker-compose_zookeeper_1            /docker-entrypoint.sh zkSe ...   Up (healthy)   2181/tcp, 2888/tcp, 3888/tcp   
```

### Working With Services

### MinIO

The MinIO client can be used to access MinIO. The `minio-client.yml` file will
create a bucket `root`, but any `mc` commands can be used to interact with MinIO
to create new buckets, delete buckets, and manage objects.

```bash
docker-compose exec minio-client mc ls
```

A full list of commands can be found in the [MinIO Client Quickstart Guide].

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
[MinIO Client Quickstart Guide]: https://docs.min.io/docs/minio-client-quickstart-guide.html

# Connecting your local database instance to superset

SQLALCHEMY URI: 
 - `clickhouse+native://default@172.24.0.1/default`
 - `clickhouse+native://default@clickhouse1/default`

When running Superset using docker or docker-compose it runs in its own docker container, as if the Superset was running in a separate machine entirely. Therefore attempts to connect to your local database with hostname localhost won't work as localhost refers to the docker container Superset is running in, and not your actual host machine. Fortunately, docker provides an easy way to access network resources in the host machine from inside a container, and we will leverage this capability to connect to our local database instance.

Here the instructions are for connecting to postgresql (which is running on your host machine) from Superset (which is running in its docker container).

1. (Mac users may skip this step) Configuring the local postgresql/database instance to accept public incoming connections. By default postgresql only allows incoming connections from localhost only, but re-iterating once again, localhosts are different for host machine and docker container. For postgresql this involves make one-line changes to the files postgresql.conf and pg_hba.conf, you can find helpful links tailored to your OS / PG version on the web easily for this task. For docker it suffices to only whitelist IPs 172.0.0.0/8 instead of *, but in any case you are warned that doing this in a production database may have disastrous consequences as you are opening your database to the public internet.

2. Instead of localhost, try using host.docker.internal (Mac users) or 172.18.0.1 (Linux users) as the host name when attempting to connect to the database. This is docker internal detail, what is happening is that in Mac systems docker creates a dns entry for the host name host.docker.internal which resolves to the correct address for the host machine, whereas in linux this is not the case (at least by default). If neither of these 2 hostnames work then you may want to find the exact host name you want to use, for that you can do ifconfig or ip addr show and look at the IP address of docker0 interface that must have been created by docker for you. Alternately if you don't even see the docker0 interface try (if needed with sudo) docker network inspect bridge and see if there is an entry for "Gateway" and note the IP address (e.g. "Gateway": "172.24.0.1").

3. If you make a configuration change to a service and run `docker-compose up` to update it, the old container is removed and the new one joins the network under a different IP address but the same name. Running containers can look up that name (e.g., "clickhouse1") and connect to the new address, but the old address stops working. If any containers have connections open to the old container, they are closed. It is a container’s responsibility to detect this condition, look up the name again and reconnect.

