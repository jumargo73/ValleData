# Usamos PostgreSQL 15 (versión recomendada para CKAN 2.11)
FROM postgres:15

# Instalamos las extensiones necesarias (PostGIS es opcional pero común)
RUN apt-get update && apt-get install -y \
    postgresql-15-postgis-3 \
    && rm -rf /var/lib/apt/lists/*


# Include extra setup scripts (eg datastore)
COPY --chown=postgres:postgres ./docker-entrypoint-initdb.d /docker-entrypoint-initdb.d

EXPOSE 5432

