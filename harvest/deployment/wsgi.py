# -*- coding: utf-8 -*-

import os
from ckan.config.middleware import make_app
from ckan.cli import CKANConfigLoader
from logging.config import fileConfig as loggingFileConfig

if os.environ.get('CKAN_INI'):
    config_path = os.environ['CKAN_INI']
else:
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), u'ckan.ini')

if not os.path.exists(config_path):
    raise RuntimeError('CKAN config file not found: {}'.format(config_path))

loggingFileConfig(config_path)
config = CKANConfigLoader(config_path).get_config()

# IMPORTANTE: Forzar la clave que está causando el TypeError
if not isinstance(config, dict):
    # Si por alguna razón es un objeto loader, extraemos el dict
    config = dict(config)

# CKAN necesita saber de qué archivo vino esta configuración
config['__file__'] = config_path


application = make_app(config)
