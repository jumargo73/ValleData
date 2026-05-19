FROM ckan/ckan-base-datapusher:0.0.21

# 1. Asegurar las rutas del entorno virtual de Python en Linux
ENV PATH="/srv/app/bin:${PATH}"
ENV VIRTUAL_ENV="/srv/app"

WORKDIR /srv/app


COPY ./deployment /srv/app/datapusher-src


USER datapusher

EXPOSE 8800

# Comando por defecto (ejemplo)
#CMD ["/srv/app/datapusher-src/bin/uwsgi", "--ini", "/srv/app/datapusher-src/deployment/datapusher-uwsgi.ini"]