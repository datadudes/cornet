Sisyphus
=====

*This is a WIP.*

Command-line tool to generate [Apache Sqoop v1](http://sqoop.apache.org/)
commands to ingest data from RDBMS databases to Hive.


# Installation

Sisyphus currently supports Postgres and MySQL.

#### Install Sisyphus with a Postgres connector

First, install Postgres dev-headers:

- Ubuntu/Debian: `apt-get install libpq-dev`
- RedHat/CentOs: `yum install postgresql-libs`
- Mac (for dev purposes): should be installed by default

Then, install Sisyphus with:

```pip install sisyphus[postgres]```

#### Install Sisyphus with a MySQL connector

First, install MySQL dev-headers:

- Ubuntu/Debian: `apt-get install python-dev libmysqlclient-dev`
- RedHat/CentOs: `yum install python-devel mysql-devel`
- Mac (for dev purposes): `brew install mysql`

Then, install Sisyphus with:

```pip install sisyphus[mysql]```

#### Install Sisyphus with both Mysql and Postgres connectors

First, install Postgres and MySQL dev-headers. Then:

```pip install sisyphus[postgres,mysql]```



