# README #

## 🏗️ Arquitectura del Repositorio

```mermaid
graph TD
    subgraph central ["PROYECTO VALLE-DATA"]
        Root[📁 valle_data] --> Conf[📁 config]
        Root --> ExtG[📁 extensions/generales]
        Root --> Harv[📁 harvest]
        Root --> Hijos[📁 Municipios/Hijos]
    end

    subgraph estructura ["Estructura por Hijo"]
        Hijos --> Alcala[alcala-ckan]
        Hijos --> Gen[nombreMunicipio-ckan]
        
        Alcala --> HCore[ckan/ckan.ini]
        Alcala --> HExt[extensions/especificas]
        
        Gen --> HCore
        Gen --> HExt
    end

    subgraph servicios ["Servicios Requeridos"]
        HCore --> DB[(PostgreSQL)]
        HCore --> Solr[Solr]
        HCore --> Redis[Redis]
    end

    Harv -.->|Cosecha| Alcala
    Harv -.->|Cosecha| Gen
```

---

# Arquitectura del Proyecto Valle-Data

```bash
valle_data/
├── ⚙️ config/               # Despliegue uWsgi (alcala-ckan-uwsgi.ini)
├── 🧩 extensions/           # Plugins Globales (Auth, LDAP, Spatial)
├── 🌾 harvest/              # Módulo de Recolección Central
│   └── 🧩 extensions/       # Plugins específicos (DCAT, Harvest)
│
├── 🏙️ alcala-ckan/          # PLANTILLA PARA HIJOS (Municipios)
│   ├── 🛠️ ckan/
│   │   └── 📄 ckan.ini      # CONFIGURACIÓN ÚNICA (DB, Solr, URL)
│   └── 🧩 extensions/       # Plugins Locales (ckanplugin)
│
└── 📄 requirements.txt      # Dependencias generales
```


--- 
## Cómo agregar un nuevo Municipio (Hijo)

1. **Clonar:** Duplica la carpeta `alcala-ckan` y cámbiale el nombre a `[nombreMunicipio]-ckan`.
2. **Configurar:** Edita el archivo `ckan/ckan.ini` dentro de la nueva carpeta:
   - Cambia `site_url` y el puerto.
   - Configura las cadenas de conexión para: `Solr`, `Datapusher`, `Redis` y `PostgreSQL`.
3. **Harvest:** Crea un nuevo Job en el módulo Harvest apuntando al `data.json` del nuevo hijo.

---
## Variables de Entorno usadas para modificar el ckan.ini del proyecto, tener en cuenta de que cada hijo y harvest tiene su propio archivo de configuracion

	#Postgres
	- POSTGRES_USER
	- POSTGRES_PASSWORD
	- POSTGRES_DB
	- CKAN_DB_USER
	- CKAN_DB_PASSWORD
	- CKAN_DB
	- DATASTORE_READONLY_USER
	- DATASTORE_READONLY_PASSWORD
	- DATASTORE_DB
	
	#Ckan
	- CKAN_SITE_ID
	- CKAN_SECRET_KEY
	- CKAN_SITE_URL
	- CKAN_SQLALCHEMY_URL	
	- CKAN_BEAKER__SESSION__SECRET
	- CKAN_API_TOKEN__JWT__ENCODE__SECRET
	- CKAN_API_TOKEN__JWT__DECODE__SECRET
	- CKAN_SOLR_URL
	- CKAN_REDIS_URL
	- CKAN_DATAPUSHER_URL
	- CKAN__DATAPUSHER__CALLBACK_URL_BASE
	- CKAN__PLUGINS
	
	# Variables de ckan.ini para el proceso del Datapusher
	- CKAN_DATASTORE_WRITE_URL
	- CKAN_DATASTORE_READ_URL
	- DATAPUSHER_API_TOKEN
	
---	

# VALLE DATA

Sistema federado de datos abiertos basado en CKAN, implementando una arquitectura **Padre - Hijos** para la gestión, publicación y federación de información institucional del departamento.

---

## Arquitectura del Sistema

El sistema se basa en la tecnología CKAN implementando un modelo federado que optimiza la gobernanza de datos regionales:

### CKAN Padre (Nodo Central)

Actúa como el núcleo de federación encargado del proceso de **Harvesting** (cosecha de metadatos).

Funciones principales:

* Consolidar el catálogo departamental.
* Federar metadatos provenientes de múltiples entidades.
* Centralizar la consulta de datasets.
* Evitar la duplicación física de recursos.
* Administrar los procesos de federación y sincronización.

### CKAN Hijos (Instancias Independientes)

Catorce (14) nodos institucionales responsables de:

* Administración de sus datasets.
* Publicación de información.
* Actualización de recursos.
* Gestión autónoma de metadatos.

Este enfoque garantiza la autonomía técnica y operativa de cada entidad participante.

---

# Instalación

La documentación completa de instalación y despliegue se encuentra disponible en:

[Documentación Técnica VALLE DATA](https://docs.google.com/document/d/1xZQ8j7tAkxGgShaVeA_ruW5f_h3JPvb4/edit?usp=drive_link&ouid=104869156579894684414&rtpof=true&sd=true&utm_source=chatgpt.com)

---

# Arquitectura de Persistencia

## Volúmenes Persistentes

### CKAN

```yaml
ckan_storage:/var/lib/ckan
pip_cache:/root/.cache/pip
site_packages:/usr/lib/python3.10/site-packages
```

### PostgreSQL

```yaml
pg_data:/var/lib/postgresql/data
```

### Solr

```yaml
solr_data:/var/solr
```

### Redis

Servicio de caché y cola de procesos.

---

# Archivos de Configuración para despliegue

## Principales

```bash
CKAN.ini
uwsgi.py
ckan-uwsgi.ini 
```

---

# Servicios Orquestados

| Servicio   | Puerto | Descripción                               |
| ---------- | ------ | ----------------------------------------- |
| Datapusher | 8800   | Procesamiento y carga automática de datos |
| Solr       | 8983   | Motor de indexación y búsqueda            |
| Redis      | 6379   | Cache y cola de tareas                    |
| CKAN       | 5000   | Portal principal                          |
| Harvest    | 5100   | Servicio de federación                    |

---

# Despliegue

Los servicios de:

* Datapusher
* CKAN
* Harvester

se despliegan mediante:

```bash
uWSGI
```

---

# Solr Core

> **Importante**
>
> Para cada instancia CKAN se debe crear un **Core** en el servicio de Apache Solr.
>
> Este espacio es utilizado por Solr para almacenar la base de datos local correspondiente a los datasets y recursos cargados en cada portal.

---

# Servicios Utilizados por Harvest

## Procesos de Federación

### fetch-consumer

Servicio encargado de descargar y procesar metadatos desde las fuentes federadas.

### gather-consumer

Servicio encargado de recopilar datasets y preparar los procesos de sincronización.

### Worker

Servicio utilizado para balanceo y procesamiento de cargas asincrónicas.

---

# Extensiones Utilizadas

## CKAN
* ckanext-ckanplugin
* ckanext-geoview
* ckanext-spatial

## Harvester
* ckanext-harvest
* ckanext-harvestplugin

## Extensiones Globales
* ckanext-auth
* ckanext-envvars
* ckanext-ldap
* ckanext-metrics_dashboard
* ckanext-report
* ckanext-dcat
* ckanext-scheming

---

# Tecnologías Utilizadas

* CKAN
* PostgreSQL
* Apache Solr
* Redis
* uWSGI
* Docker
* Linux Ubuntu

---

# Objetivo del Proyecto

VALLE DATA busca consolidar un ecosistema interoperable de datos abiertos que permita:

* Centralizar la consulta de información pública.
* Facilitar procesos de interoperabilidad institucional.
* Garantizar autonomía tecnológica de cada entidad.
* Implementar procesos de federación escalables.
* Mejorar el acceso y reutilización de datos abiertos.

---

# Notas Técnicas

* Cada instancia CKAN debe contar con:

  * Base de datos PostgreSQL independiente.
  * Core Solr independiente.
  * Configuración propia de Harvest.
  * Volúmenes persistentes dedicados.

* El nodo Padre únicamente federa metadatos y no duplica físicamente los archivos publicados por los nodos Hijos.

* Los procesos Harvest se ejecutan de forma asincrónica mediante workers y consumidores especializados.

___
#Innstalar la APP en el Sistema
Activar el Entorno Virtual
. /usr/lib/ckan/default/bin/activate

cd /usr/lib/ckan/default/src/valle_data
pip install -r requiriments.txt --no-deps --force-reinstall


#Reconstruir los asset para Ckan(ejemplo alcala)
Si tu ruta de de trabajo (Entorno Virtual) es  /usr/lib/ckan/default/ y el directorio de trabajo es /usr/lib/ckan/default/src/

rm -rf /usr/lib/ckan/default/src/valle_data/alcala-ckan/ckan/public/webassets/*
/usr/lib/ckan/default/bin/ckan -c /usr/lib/ckan/default/src/valle_data/alcala-ckan/ckan/ckan.ini asset build
chmod -R 775 /var/lib/ckan/

#Reportes Aplica a Harvest
/usr/lib/ckan/default/bin/ckan -c /usr/lib/ckan/default/src/valle_data/harvest/ckan/ckan.ini report generate reporte-federacion
http://<url>/report/reporte-federacion
/usr/lib/ckan/default/bin/ckan -c /usr/lib/ckan/default/src/valle_data/harvest/ckan/ckan.ini report metrics-dashboard
http://<url>/report/metrics-dashboard


# Autor

Proyecto desarrollado para la federación de datos abiertos del departamento del Valle del Cauca.
Ingeniero Julian Gonzalez y Ingenieroa Paula Quevedo