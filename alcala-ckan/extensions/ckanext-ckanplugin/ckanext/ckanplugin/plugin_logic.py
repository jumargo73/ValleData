import ckan.plugins as p
import ckan.plugins.toolkit as tk
from flask import Blueprint, request
import logging
import os
import ckanext.ckanplugin.logic.action.resourceRating as rating_action
import ckanext.ckanplugin.logic.auth.resourceRating as rating_auth
import ckanext.ckanplugin.logic.action.comments as comments
import ckanext.ckanplugin.logic.auth.comments as comments_auth
import ckanext.ckanplugin.logic.action.get as getAction
import ckanext.ckanplugin.logic.action.update as updateAction



import ckanext.ckanplugin.logic.auth.get as getAuth
import ckanext.ckanplugin.logic.auth.update as updateAuth
import ckanext.ckanplugin.model.package_ext as package_ext
import ckanext.ckanplugin.model as model
import ckanext.ckanplugin.helpers as helpers
from typing import Any
from ckan.types import Context 
from ckan.model import Session
from ckan.plugins.toolkit import DefaultDatasetForm
from ckan.logic.schema import default_create_package_schema
from ckan.logic.schema import default_update_package_schema
from ckan.logic.schema import default_show_package_schema
from ckanext.ckanplugin.services.geojson_converter import GeoJSONConverter  
from ckanext.ckanplugin.views.estadistica import estadistica
from ckanext.ckanplugin.views.noticias import noticias
from ckanext.ckanplugin.views.contador import contador
from ckan.plugins.interfaces import IClick 
import ckanext.ckanplugin.model



log = logging.getLogger(__name__)


class CkanPlugin(DefaultDatasetForm,p.SingletonPlugin):
   
    p.implements(p.IConfigurer, inherit=True)   
    p.implements(p.IActions) 
    p.implements(p.IAuthFunctions)
    p.implements(p.ITemplateHelpers)   
    p.implements(p.IDatasetForm, inherit=True)
    p.implements(p.IBlueprint)
    p.implements(IClick)
   
    
    def get_blueprint(self):
      
        # Blueprint 2
        download_bp = Blueprint(
            "download_tracker",
            __name__
        )

        
        return [estadistica,noticias]
    
    
    def get_commands(self):
        # Retorna una lista vacía para indicarle a CKAN 
        # que este plugin no inyecta comandos nuevos
        return []
    
    def hello_angular(self):
        return tk.render('/home/index.html')
        
    def update_config(self, config):

        log.warning("[CkanPlugin][update_config] ejecutado")

        if not getattr(config, '_ckanplugin_loaded', False):
            tk.add_template_directory(config, 'templates')                          
            tk.add_public_directory(config, 'public')
            tk.add_resource('public','ckanext-ckanplugin')

            config._ckanplugin_loaded = True

    def get_db_functions(self):
        # Al retornar True o un diccionario vacío, le avisas al core 
        # que indexe la carpeta 'migration/' interna de esta extensión
        return {}

    def package_types(self):
        log.warning("[CkanPlugin][package_types] ejecutado") 
        return ['reporte_dataset']

    def is_fallback(self):
        print("🔥 is_fallback ejecutado")
        return True    

    def create_package_schema(self):
        schema = super().create_package_schema()

        schema.update({
            'city': [
                tk.get_validator('ignore_empty'),
                tk.get_converter('convert_to_extras')
            ],
            'department': [
                tk.get_validator('ignore_empty'),
                tk.get_converter('convert_to_extras')
            ],
            'update_frequency': [
                tk.get_validator('ignore_empty'),
                tk.get_converter('convert_to_extras')
            ],
        })

        return schema


    def update_package_schema(self):
        schema = super().update_package_schema()

        schema.update({
            'city': [
                tk.get_validator('ignore_empty'),
                tk.get_converter('convert_to_extras')
            ],
            'department': [
                tk.get_validator('ignore_empty'),
                tk.get_converter('convert_to_extras')
            ],
            'update_frequency': [
                tk.get_validator('ignore_empty'),
                tk.get_converter('convert_to_extras')
            ],
        })

        return schema


    def show_package_schema(self):
        schema = super().show_package_schema()

        schema.update({
            'city': [
                tk.get_converter('convert_from_extras'),
                tk.get_validator('ignore_missing')
            ],
            'department': [
                tk.get_converter('convert_from_extras'),
                tk.get_validator('ignore_missing')
            ],
            'update_frequency': [
                tk.get_converter('convert_from_extras'),
                tk.get_validator('ignore_missing')
            ],
        })

        return schema
   
    def get_actions(self):
        return {
            'resource_rating_set': rating_action.resource_rating_set,
            'resource_rating_get': rating_action.resource_rating_get,
            'comments_set': comments.comments_set,
            'comments_get': comments.comments_get,
            'guardar_contador':updateAction.guardar_contador  
        }    

    def get_auth_functions(self):
        return {
            'resource_rating_set': rating_auth.resource_rating_set,
            'resource_rating_get': rating_auth.resource_rating_get,
            'comments_set': comments_auth.comments_set,
            'comments_get': comments_auth.comments_get,
            'guardar_contador':updateAuth.guardar_contador  
        }

    def get_helpers(self):
        return {
            "obtener_contador_package": helpers.obtener_contador_package,
            "obtener_contador_resource": helpers.obtener_contador_resource,
            "guardar_contador": helpers.guardar_contador,
            "get_featured_noticia":helpers.get_featured_noticia,
            "get_featured_general":helpers.get_featured_general,
            "get_featured_estadistica":helpers.get_featured_estadistica,
            "get_featured_dataset":helpers.get_featured_dataset,
            "get_featured_groups_new":helpers.get_featured_groups_new,
            "contar_visualizacion":helpers.contar_visualizacion,
            "contar_descargas":helpers.contar_descargas,
        } 

     
        
    
    
    
