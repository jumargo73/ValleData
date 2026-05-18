#!/bin/bash
set -e

# Crear el usuario de solo lectura
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE "$DATASTORE_READONLY_USER" WITH NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN PASSWORD '$DATASTORE_READONLY_PASSWORD';
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) ALCALA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_DB" TO "$CKAN_DB_USER";
EOSQL
