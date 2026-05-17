from alembic.config import Config
from alembic import command
import os
from flask import current_app

migration_path = "/srv/app/src/alcala-ckan/ckan/ckanext/ckanplugin/migration/ckan"
sqlalchemy_url = current_app.config.get('sqlalchemy.url')

cfg = Config(os.path.join(migration_path, "alembic.ini"))

# PON TU URL REAL AQUÍ
cfg.set_main_option("sqlalchemy.url", sqlalchemy_url)

command.upgrade(cfg, "head")