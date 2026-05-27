#!/bin/bash
set -e

# Crear el usuario de solo lectura
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE "$DATASTORE_READONLY_USER" WITH NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN PASSWORD '$DATASTORE_READONLY_PASSWORD';
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) ARGELIA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_ARGELIA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_ARGELIA_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) ALCALA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_ALCALA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_ALCALA_DB" TO "$CKAN_DB_USER";
EOSQL


# Crear la base de datos del datastore (asignando al dueño de CKAN) BOLIVAR
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_BOLIVAR_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_BOLIVAR_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) EL_AGUILA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_EL_AGUILA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_EL_AGUILA_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) EL_CERRITO
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_EL_CERRITO_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_EL_CERRITO_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) GUACARI
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_GUACARI_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_GUACARI_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) LA_VICTORIA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_LA_VICTORIA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_LA_VICTORIA_DB" TO "$CKAN_DB_USER";
EOSQL


# Crear la base de datos del datastore (asignando al dueño de CKAN) PRADERA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_PRADERA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_PRADERA_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) RIOFRIO
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_RIOFRIO_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_RIOFRIO_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) SAN_PEDRO
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_SAN_PEDRO_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_SAN_PEDRO_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) TRUJILLO
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_TRUJILLO_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_TRUJILLO_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) ULLOA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_ULLOA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_ULLOA_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) VIJES
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_VIJES_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_VIJES_DB" TO "$CKAN_DB_USER";
EOSQL

# Crear la base de datos del datastore (asignando al dueño de CKAN) YOTOCO
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DATASTORE_YOTOCO_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# Dar permisos iniciales básicos
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DATASTORE_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$DATASTORE_YOTOCO_DB" TO "$CKAN_DB_USER";
EOSQL

