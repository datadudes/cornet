Cornet [![Build Status](https://travis-ci.org/datadudes/cornet.svg?branch=master)](https://travis-ci.org/datadudes/cornet) [![Coverage Status](https://coveralls.io/repos/datadudes/cornet/badge.svg?branch=master)](https://coveralls.io/r/datadudes/cornet?branch=master)
=====


*This is a WIP.*

Command-line tool to generate [Apache Sqoop v1](http://sqoop.apache.org/)
commands to ingest data from RDBMS databases to Hive.


# Installation

Cornet currently supports Postgres and MySQL.

#### Install Cornet with a Postgres connector

First, install Postgres dev-headers:

- Ubuntu/Debian: `apt-get install libpq-dev`
- RedHat/CentOs: `yum install postgresql-libs`
- Mac (for dev purposes): should be installed by default

Then, install Cornet with:

```pip install cornet[postgres]```

#### Install Cornet with a MySQL connector

First, install MySQL dev-headers:

- Ubuntu/Debian: `apt-get install python-dev libmysqlclient-dev`
- RedHat/CentOs: `yum install python-devel mysql-devel`
- Mac (for dev purposes): `brew install mysql`

Then, install Cornet with:

```pip install cornet[mysql]```

#### Install Cornet with both Mysql and Postgres connectors

First, install Postgres and MySQL dev-headers. Then:

```pip install cornet[postgres,mysql]```



