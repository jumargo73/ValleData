FROM python:3.10-slim

USER root

# 1. Dependencias de sistema
RUN apt-get update && apt-get install -y \
    git \	
    build-essential \
    libxslt1-dev \
    libxml2-dev \
    zlib1g-dev \
    libffi-dev \
    python3-dev \
	libpcre2-8-0 \
    libpcre2-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Configurar Locales
RUN apt-get update && apt-get install -y locales && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8	

# 3. Directorio de trabajo
RUN mkdir -p /srv/app/datapusher-src
WORKDIR /srv/app/datapusher-src

# 3.1 Permisos Directorio de trabajo
RUN useradd -r -m -s /bin/false datapusher && \
    chown -R datapusher:datapusher /srv/app/datapusher-src && \
    chmod -R 755 /srv/app/datapusher-src
	

# 4. Clonar código PRIMERO
RUN git clone https://github.com/ckan/datapusher.git .

# 5. Crear entorno virtual en una ruta distinta o después del clone
ENV VENV=/srv/app/datapusher-src
ENV PATH="$VENV/bin:$PATH"

RUN python3 -m venv /srv/app/datapusher-src/

RUN echo "import warnings; \
from requests.packages.urllib3.exceptions import InsecureRequestWarning; \
warnings.filterwarnings('ignore', category=SyntaxWarning); \
try: from requests import RequestsDependencyWarning; warnings.filterwarnings('ignore', category=RequestsDependencyWarning) \
except: pass" > $(find $VENV/lib/ -name "site-packages")/sitecustomize.py

RUN find $VENV/lib/ -name "any.py" -exec sed -i "s/is not ''/!= ''/g" {} +

# 5.1 Asegurar específicamente que los binarios sean ejecutables
RUN chmod +x /srv/app/datapusher-src/bin/*

# 6. Instalar dependencias usando la ruta absoluta al python del venv
RUN $VENV/bin/python -m pip install --upgrade pip && \
    $VENV/bin/python -m pip install uwsgi && \
    $VENV/bin/python -m pip install -r requirements.txt && \
    $VENV/bin/python -m pip install -e .
	
RUN $VENV/bin/pip install --force-reinstall \
	"requests==2.27.1" \
	"urllib3==1.26.15" \
	"charset-normalizer==2.0.12" \
	"idna==3.4"

# 7. APLICAR EL PARCHE DE MAPPING (Python 3.10 compatibilidad)
# Esto busca en el lib del venv y corrige la importación de collections
RUN find $VENV/lib/ -name "*.py" -exec sed -i 's/from collections import Mapping/from collections.abc import Mapping/g' {} + && \
    find $VENV/lib/ -name "*.py" -exec sed -i 's/from collections import MutableMapping/from collections.abc import MutableMapping/g' {} +

COPY ./deployment /srv/app/datapusher-src/deployment

USER datapusher

EXPOSE 8800

# Comando por defecto (ejemplo)
CMD ["/srv/app/datapusher-src/bin/uwsgi", "--ini", "/srv/app/datapusher-src/deployment/datapusher-uwsgi.ini"]




