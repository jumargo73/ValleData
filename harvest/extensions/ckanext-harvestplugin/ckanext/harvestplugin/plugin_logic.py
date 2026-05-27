import ckan.plugins as p
import ckan.plugins.toolkit as tk
from flask import Blueprint, request, jsonify,current_app,redirect
import logging
from ckan.model import Package
from sqlalchemy import Column, Unicode
import os
from typing import Any
from ckan.types import Context 
from ckan.model import Session
from ckan.plugins.toolkit import DefaultDatasetForm
from ckan.logic.schema import default_create_package_schema
from ckan.logic.schema import default_update_package_schema
from ckan.logic.schema import default_show_package_schema
from ckanext.report.interfaces import IReport
from collections import OrderedDict
import ckanext.harvestplugin.lib.helpers as helpers
from ckanext.harvestplugin.views.estadistica import estadistica
from ckanext.harvestplugin.views.noticias import noticias
from ckanext.harvestplugin.reports.report_logic import reporte_federacion_global
import ckan.lib.i18n as i18n
import ckan.lib.helpers as h




log = logging.getLogger(__name__)



class HarvestPlugin(DefaultDatasetForm,p.SingletonPlugin):
   
    p.implements(p.IConfigurer, inherit=True)   
    p.implements(p.IDatasetForm, inherit=True)
    p.implements(p.ITemplateHelpers) 
    p.implements(IReport)
    p.implements(p.IBlueprint)
    p.implements(p.ITranslation)
    

    def update_config(self, config):

        log.warning("[HarvestPlugin][update_config] ejecutado")

        if not getattr(config, '_ckanplugin_loaded', False):
            tk.add_template_directory(config, 'templates')                          
            tk.add_public_directory(config, 'public')
            tk.add_resource('public','ckanext-harvestplugin')

            config._ckanplugin_loaded = True

    
      # Este mÃ©todo le dice a CKAN que sume las traducciones de la extensiÃ³n al core
    def i18n_directory(self):
        import os
        return os.path.join(os.path.dirname(__file__), 'i18n')

    def i18n_locales(self):
        # Idiomas que soporta tu extensiÃ³n (ej: ['es', 'en', 'fr'])
        return ['es', 'en']

    def i18n_domain(self):
        # El identificador Ãºnico de traducciones para tu extensiÃ³n
        return 'ckanext-harvestplugin'

    def get_commands(self):
        # Retorna una lista vacÃ­a para indicarle a CKAN 
        # que este plugin no inyecta comandos nuevos
        return []
    
    def get_blueprint(self):
        return [estadistica,noticias]
        
    
    def package_types(self):
        log.warning("[HarvestPlugin][package_types] ejecutado") 
        return ['dataset']

    def is_fallback(self):
        print("Ã°ÂÂÂ¥ is_fallback ejecutado")
        return True    

    def create_package_schema(self):
        schema = super().create_package_schema()
        return schema


    def update_package_schema(self):
        schema = super().update_package_schema() 
        return schema


    def show_package_schema(self):
        schema = super().show_package_schema()
        return schema
        
    def get_helpers(self):
        return {
            "get_site_statistics":helpers.get_site_statistics,
            "get_featured_noticia":helpers.get_featured_noticia,
            "get_featured_general":helpers.get_featured_general,
            "get_featured_estadistica":helpers.get_featured_estadistica,
            "get_featured_dataset":helpers.get_featured_dataset,
            "get_featured_groups_new":helpers.get_featured_groups_new,
            'obtener_idiomas_portales': i18n.get_locales,
            "get_locales_dict":i18n.get_locales_dict    
        }     
     
        
    # LÃÂ­nea 34: AsegÃÂºrate de que el mÃÂ©todo tenga 4 espacios desde el inicio de la lÃÂ­nea
    def register_reports(self):
        return [
            {
                'name': 'reporte-federacion',
                'title': 'Reporte de Datos Federados (Harvest)',
                'description': 'Muestra el arbol completo de nodos origen, dependencias y datasets.',
                'generate': reporte_federacion_global,
                'option_defaults': {}, 
                # Se transforma en una funciÂ¨Â®n ejecutable (lambda) que retorna la lista
                'option_combinations': lambda: [{}],
                'template': 'report/reporte_federacion.html'
            }
        ]

   
