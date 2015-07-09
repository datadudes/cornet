Cornet [![Build Status](https://travis-ci.org/datadudes/cornet.svg?branch=master)](https://travis-ci.org/datadudes/cornet) [![Coverage Status](https://coveralls.io/repos/datadudes/cornet/badge.svg?branch=master)](https://coveralls.io/r/datadudes/cornet?branch=master)
=====

*Cornet* is a command-line tool on top of [Apache Sqoop (v1)](http://sqoop.apache.org/) to simplify ingestion of data from RDBMs to Hive (main author).

Cornet is a generator of Sqoop commands. If you are a data engineer using Sqoop and you find yourself writing hundreds of Sqoop commands which are hard to maintain and update, Cornet might be of great help to you.

## Features

Ingest tables from RDBMS to Hive u

- type-based java-type-mapping and hive-type-mapping
- skip selected tables
- import only selected tables


## Cornet: First steps

Cornet needs a configuration file in a [YAML](http://en.wikipedia.org/wiki/YAML) format. Here's an example of the most simple config file called `example.yaml`:

```
- source:
    host: db-server.example.com
    port: 5432
    db: portal
    user: marcel
    password: my-secret-password
    driver: postgres
  hive:
    db: source
```

Assume the PostgreSQL database contains tables `customers` and `products`. Calling `cornet example.yaml` then generates the following to stdout:

```
sqoop import \
    --table customers \
    --hive-table source.customers \
    --hive-import \
    --connect jdbc:postgresql://db-server.example.com:5432/portal \
    --username marcel \
    --password my-secret-password

sqoop import \
    --table products \
    --hive-table source.products \
    --connect jdbc:postgresql://db-server.example.com:5432/portal \
    --hive-import \
    --username marcel \
    --password my-secret-password
```

This output can be then run on the Hadoop cluster, for instance as follows:

```
cornet example.yaml > sqoop_commands.sh
chmod +x sqoop_commands.sh
./sqoop_commands.sh
```

This example by itself does not solve any pain point. However, checkout the [Features](#features) section for the cool features that we have built in.


## Cool features

### Type-based column mapping

Out of the box, Sqoop supports only standard JDBC column types. For other types, e.g. `varbinary` in MySQL or `UUID` in Postgres, you need to add a `--map-column-hive` and `--map-column-java` parameter to Sqoop. Unfortunately, *Sqoop expect the mapping for columns rather than types*.

- as of Sqoop 1.45, the only way to ingest such data is to write a separate Sqoop command *for each table*, with the column mapping specified. In case of large databases, this might lead to thousands of Sqoop commands needed.
- if a new column with a non-standard type is added, Sqoop ingestion fails

Cornet solves this problem by providing a type-based mapping. Use the `type-mapping` section as follows:

```
- source:
    host: db-server.example.com
    db: portal
    ...
  map_types:
    java:
      VARBINARY: String
      UUID: String
    hive:
      VARBINARY: String
      UUID: String
```

Using this configuration, if there are any `VARBINARY` or `UUID` columns present in the `portal` database, Cornet will add `--map-column-java` and `--map-column-hive` to the corresponding Sqoop commands. For example:

```
sqoop import \
    --table products \
    --map-column-java customer_id=String,some_blob_column=String \
    --map-column-hive customer_id=String,some_blob_column=String \
    ...
```


### Powerful selection of tables, including regexp-based filtering

If you don't need to import all tables from a database, use the `skip_tables` section. For example:

```
- source:
    host: db-server.example.com
    db: portal
    ...
  skip_tables:
    - schema_version
    - log
```

The tables are are actually regular expressions. For instance, you can simply exclude all tables starting a prefix `QUARTZ_` as follows:

```
  skip_tables:
    - QUARTZ_.*
```

Similarly, there's a `import_tables` which allows you to import only selected list of tables:

### Add a prefix to Hive tables

### Add arbitrary Sqoop parameters

### Override Sqoop parameters on a per-table basis

### Support for password-file

### Don't repeat yourself: Meet the `global` section

### It's all Jinja!

The YAML config files are actually [Jinja2](http://jinja.pocoo.org/docs/dev/) templates! This might come very handy.

For example, you can ingest databases with a similar name using the [for-cycle](http://jinja.pocoo.org/docs/dev/templates/#for):

```
{% for country in ['us', 'gb', 'fr'] %}
- source:
    db: portal_{{country}}
  hive:
    table_prefix: 'portal_{{country}}_'
{% endfor %}
```

To make the YAML config file even more DRY, checkout the Jinja2 [variables](http://jinja.pocoo.org/docs/dev/templates/#assignments) and [blocks](http://jinja.pocoo.org/docs/dev/templates/#assignments) and [many other features](http://jinja.pocoo.org/docs/dev/templates/#) that Jinja2 provides.

### Explanatory syntax errors

We have tried out best to provide good explanatory messages if there is something missing or not quite right in the config file.


## Installation

_Cornet currently supports Postgres and MySQL. Please [create an issue](https://github.com/datadudes/cornet/issues/new) if you need support for other databases._

First, install dev-headers for the source database you plan to ingest into Hive:

#### Postgres

- Ubuntu/Debian: `apt-get install libpq-dev`
- RedHat/CentOs: `yum install postgresql-libs`
- Mac OS: should be installed by default

#### MySQL

- Ubuntu/Debian: `apt-get install python-dev libmysqlclient-dev`
- RedHat/CentOs: `yum install python-devel mysql-devel`
- Mac OS: `brew install mysql`

Then, install Cornet with `pip`, with desired connectors in the brackets:

- Cornet with Postgres: `pip install cornet[postgres]`
- Cornet with MySQL: `pip install cornet[mysql]`
- Cornet with MySQL and Postgres: `pip install cornet[mysql,postgres]`


## Issues and contributions

Please [create an issue](https://github.com/datadudes/cornet/issues/new) if you encounter any problem or need an additional feature. We'll try to get back to you as soon as possible.

## Authors

Created with passion by [Marcel](https://github.com/mkrcah)
and [Daan](https://github.com/DandyDev).
