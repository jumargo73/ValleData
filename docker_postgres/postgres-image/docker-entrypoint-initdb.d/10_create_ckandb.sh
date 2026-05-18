#!/bin/bash
set -e

# 1. Crear el usuario/rol de CKAN
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE "$CKAN_DB_USER" WITH NOSUPERUSER CREATEDB CREATEROLE LOGIN PASSWORD '$CKAN_DB_PASSWORD';
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) harvest
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_DB" TO "$CKAN_DB_USER";
EOSQL


# 2. Crear la base de datos (con el dueño ya asignado) alcala
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_ALCALA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_ALCALA_DB" TO "$CKAN_DB_USER";
EOSQL

