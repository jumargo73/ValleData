# Usamos Solr 9 como base (versión recomendada para CKAN 2.11)
FROM ckan/ckan-solr:2.10-solr9

# Cambiamos a usuario root para configurar el core
USER root

# Creamos el directorio para el core de CKAN
RUN mkdir -p /var/solr/data/ckan/conf

# Descargamos el esquema oficial de CKAN 2.11.4
# Nota: CKAN usa un managed-schema o schema.xml personalizado
COPY ./schema/schema.xml  /var/solr/data/ckan/conf/managed-schema

# Copiamos la configuración predeterminada de Solr para completar el core
RUN cp -r /opt/solr/server/solr/configsets/_default/conf/* /var/solr/data/ckan/conf/ && \
    chown -R solr:solr /var/solr/data/ckan

# Volvemos al usuario solr por seguridad
USER solr

# Exponemos el puerto estándar
EXPOSE 8983
