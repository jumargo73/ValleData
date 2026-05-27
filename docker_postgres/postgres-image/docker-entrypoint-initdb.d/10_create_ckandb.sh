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


# 2. Crear la base de datos (con el dueño ya asignado) ARGELIA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_ARGELIA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_ARGELIA_DB" TO "$CKAN_DB_USER";
EOSQL


# 2. Crear la base de datos (con el dueño ya asignado) alcala
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_ALCALA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_ALCALA_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) BOLIVAR
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_BOLIVAR_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_BOLIVAR_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) EL_AGUILA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_EL_AGUILA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_EL_AGUILA_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) EL_CERRITO
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_EL_CERRITO_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_EL_CERRITO_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) GUACARI
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_GUACARI_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_GUACARI_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) LA_VICTORIA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_LA_VICTORIA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_LA_VICTORIA_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) PRADERA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_PRADERA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_PRADERA_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) RIOFRIO
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_RIOFRIO_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_RIOFRIO_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) SAN_PEDRO
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_SAN_PEDRO_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_SAN_PEDRO_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) TRUJILLO
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_TRUJILLO_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_TRUJILLO_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) ULLOA
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_ULLOA_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_ULLOA_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) VIJES
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_VIJES_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_VIJES_DB" TO "$CKAN_DB_USER";
EOSQL

# 2. Crear la base de datos (con el dueño ya asignado) YOTOCO
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$CKAN_YOTOCO_DB" OWNER "$CKAN_DB_USER" ENCODING 'UTF-8';
EOSQL

# 3. Otorgar privilegios (opcional pero recomendado)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$CKAN_YOTOCO_DB" TO "$CKAN_DB_USER";
EOSQL
