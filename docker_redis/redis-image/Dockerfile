# Usamos la imagen oficial de Redis 7 basada en Alpine (más ligera)
FROM redis:7-alpine

# Opcional: Copiar un archivo de configuración personalizado si lo tienes
# COPY redis.conf /usr/local/etc/redis/redis.conf

# Exponer el puerto por defecto
EXPOSE 6379

# Comando para iniciar Redis con persistencia activada
# Esto es vital para que CKAN no pierda datos de tareas en cola si Redis se reinicia
CMD ["redis-server", "--appendonly", "yes"]
