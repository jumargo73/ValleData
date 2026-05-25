import ckan.plugins.toolkit as tk
from flask import Blueprint
import ckanext.ckanplugin.helpers as helpers
import logging

log = logging.getLogger(__name__)

import logging
contador = Blueprint(
    'contador', 
    __name__,   
    url_prefix='/contador'
)

@contador.route('/dataset/<dataset>/resource/<resource_id>/download/<filename>')
def resource_download(dataset, resource_id, filename):

    log.info("[views][contador][resource_download] ejecutado")

    # 1. Ejecuta tu lógica de guardado de forma segura
    try:
        helpers.guardar_contador(dataset, resource_id, 'Download')
    except Exception as e:
        log.error(f"Error al guardar el contador: {str(e)}")

    # 2. Redirige de forma invisible al descargador oficial de CKAN
    # CKAN internamente mapea el paquete con el parámetro 'id'
    return tk.redirect_to(
        'resource.download',
        id=dataset,
        resource_id=resource_id,
        filename=filename
    )
