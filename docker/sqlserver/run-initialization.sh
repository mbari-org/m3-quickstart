#!/usr/bin/env bash

# Wait to be sure that SQL Server came up
sleep 90s

# Run the setup script to create the DB and the schema in the DB
# Note: make sure that your password matches what is in the Dockerfile
#/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -d master -i create-database.sql

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

for f in $(ls "$MY_DIR/docker-entrypoint-initdb.d/*.sql") 
do 
  /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -d master -i "$f"
done