import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.model as model_ckan
from flask import Blueprint, request,g
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


class CkanPluginLogin(DefaultDatasetForm,p.SingletonPlugin):
   
    p.implements(p.IConfigurer, inherit=True)   
    p.implements(p.IActions) 
    p.implements(p.IAuthFunctions)
    p.implements(p.ITemplateHelpers)   
    p.implements(p.IDatasetForm, inherit=True)
    p.implements(p.IBlueprint)
    p.implements(IClick)
   

    #log.info("[ckanplugin][CkanPluginLogin] Cargado con Exito")
   
    
    def get_blueprint(self):
      
        # Blueprint 2
        bp = Blueprint('contador_datastore', __name__)

        @bp.before_app_request
        def interceptar_dump_datastore():
            if request and request.path:
                path = request.path.lower()
                
                # Buscamos si la URL es un dump del Datastore
                if "/datastore/dump/" in path:
                    # Extraemos el resource_id desde la URL (/datastore/dump/<resource_id>)
                    parts = path.strip('/').split('/')
                    if len(parts) >= 3:
                        resource_id = parts[2]
                        
                        # Candado 'g' para evitar duplicados si la petición rebucea internamente
                        download_flag = f"processed_datastore_dump_{resource_id}"
                        
                        if not getattr(g, download_flag, False):
                            setattr(g, download_flag, True)
                            
                            #log.info(f"[contador] ACCIÓN DETECTADA: Descarga Datastore Dump de {resource_id}")
                            try:
                                resource = model_ckan.Resource.get(resource_id)
                                
                                if resource:
                                    package_id = resource.package_id
                                    #log.info(f"[contador] Relación encontrada: Recurso {resource_id} -> Paquete {package_id}")
                                    
                                    # Ejecutamos tu función helper 100% funcional con los datos completos
                                    helpers.guardar_contador(package_id, resource_id, 'Download')
                                else:
                                    log.warning(f"[contador] El recurso {resource_id} no existe en la base de datos central.")                               
                              
                            except Exception as e:
                                log.error(f"Error en contador de descarga datastore: {str(e)}")
             

        
        return [bp,estadistica,noticias,contador]
    
    
    def get_commands(self):
        # Retorna una lista vacía para indicarle a CKAN 
        # que este plugin no inyecta comandos nuevos
        return []
    
    def hello_angular(self):
        return tk.render('/home/index.html')
        
    def update_config(self, config):

        #log.warning("[CkanPlugin][update_config] ejecutado")

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
        #log.warning("[CkanPlugin][package_types] ejecutado") 
        return ['reporte_dataset']

    def is_fallback(self):
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

     
class CkanPluginPackageResourcePlugin(p.SingletonPlugin):
    p.implements(p.IResourceController)
    p.implements(p.IPackageController)
    p.implements(p.IDatasetForm)
   
    
    #log.info("[ckanplugin][CkanPluginPackageResourcePlugin] Cargado con Exito")
    
    
    # --- resource_create ---        
    def before_resource_create(self,context: Context, resource: dict[str, Any]):
        #log.info("[ckanplugin][CkanPluginPackageResourcePlugin][before_resource_create] ¡Evento capturado!")
        pass

    def after_resource_create(self,context: Context, resource: dict[str, Any]):
        #log.info("[ckanplugin][CkanPluginPackageResourcePlugin][after_resource_create] ¡Evento capturado!")
        pass
        
    # --- dataset_create ---     
    def after_dataset_create(self,context: Context,  pkg_dict: dict[str, Any]):
        #log.info("[ckanplugin][CkanPluginPackageResourcePlugin][after_dataset_create] ¡Evento capturado!")
        return pkg_dict
    
    # --- resource_update ---    

    def before_resource_update(self,context: Context, current: dict[str, Any], resource: dict[str, Any]):
        #log.info("[ckanplugin][CkanPluginPackageResourcePlugin][before_resource_update] ¡Evento capturado!")
        pass

    def after_resource_update(self, context, resource):
        #log.info("[ckanplugin][CkanPluginPackageResourcePlugin][after_resource_update] ¡Evento capturado!")
        pass
    
    # --- dataset_update ---
    
    def after_dataset_update(self,context: Context, pkg_dict: dict[str, Any]):
        pass

    # --- resource_delete ---
        
    def before_resource_delete(self,context: Context, resource: dict[str, Any], resources: list[dict[str, Any]]):
        #log.info("[ckanplugin][CkanPluginPackageResourcePlugin][before_resource_delete] ¡Evento capturado!")
        pass

    def after_resource_delete(self,context: Context, resources: list[dict[str, Any]]):
        #log.info("[ckanplugin][CkanPluginPackageResourcePlugin][after_resource_delete] ¡Evento capturado!")
        pass

    # --- dataset_delete ---
    def after_dataset_delete(self,context: Context, pkg_dict: dict[str, Any]):
        pass
    
    # --- resource_show ---
    
    def before_resource_show(self,resource_dict: dict[str, Any]):
        #log.info("[ckanplugin][CkanPluginPackageResourcePlugin][before_resource_show] ¡Evento capturado!")
        
        try:
            # Extraemos los IDs necesarios del diccionario del recurso
            package_id = resource_dict.get('package_id')
            resource_id = resource_dict.get('id')
            
            # Ejecutas tu lógica de guardado
            helpers.guardar_contador(package_id, resource_id, 'Download')
            
        except Exception as e:
            log.error(f"Error al guardar en el contador: {str(e)}") 
        return resource_dict

    def before_dataset_show(self,context: Context, pkg_dict: dict[str, Any]):
        return pkg_dict
    
    
    # --- dataset_show ---   
    def after_dataset_show(self,context: Context, pkg_dict: dict[str, Any]):
        return pkg_dict
        
    def before_dataset_view(self,pkg_dict: dict[str, Any]):
        return pkg_dict  
        
    # --- dataset_search ---    
    def before_dataset_search(self,search_params: dict[str, Any]):
        return search_params    
    
    def before_resource_search(self,search_params: dict[str, Any]):
        return search_params  

    def after_dataset_search(self,search_results: dict[str, Any], search_params: dict[str, Any]):
       return search_results
        
    
    def after_resource_search(self,context: Context,data_dict: dict[str, Any], search_params: dict[str, Any]):
        #log.info("[ckanplugin][CkanPluginPackageResourcePlugin][after_resource_search] ¡Evento capturado!")
        return data_dict
       
    
    # --- dataset_index ---   
    
    def before_dataset_index(self,pkg_dict: dict[str, Any]):
        return pkg_dict
    
    
    # --- create ---   
    def create(self,entity: model_ckan.Package):
        pass
    
    # --- delete ---  
    def delete(self,entity: model_ckan.Package):
        pass
    
    # --- create ---
    def edit(self,entity: model_ckan.Package):
        pass        
        
    # --- READ ---      
    def read(self,entity: model_ckan.Package):
        #log.info("[ckanplugin][CkanPluginPackageResourcePlugin][read] ¡Evento capturado!")
        pass


    def before_resource_view(self, *args, **kwargs):
        pass
        #log.info("[ckanplugin][contador][before_resource_view] Vista de recurso detectada")
        
    def before_resource_show(self, *args, **kwargs):
        # 1. Extraemos el diccionario del recurso de forma segura
        res_dict = args[1] if len(args) > 1 and isinstance(args[1], dict) else (args[0] if args and isinstance(args[0], dict) else kwargs.get('resource_dict'))
        
        if not res_dict:
            return args[1] if len(args) > 1 else (args[0] if args else None)

        package_id = res_dict.get('package_id')
        resource_id = res_dict.get('id')

        #log.info(f"[ckanplugin][CkanPluginPackageResourcePlugin][before_resource_view] request: {request}")
        #log.info(f"[ckanplugin][CkanPluginPackageResourcePlugin][before_resource_view] package_id: {package_id}")         
        #log.info(f"[ckanplugin][CkanPluginPackageResourcePlugin][before_resource_view] resource_id: {resource_id}")
        # 2. FILTRAR EL TRÁFICO: Solo actuar ante interacciones reales del usuario en la web
        if request and request.path and request.endpoint:
            path = request.path.lower().rstrip('/')
            endpoint = request.endpoint.lower()   
            #log.info(f"[ckanplugin][CkanPluginPackageResourcePlugin][before_resource_view] path: {path}")         
            #log.info(f"[ckanplugin][CkanPluginPackageResourcePlugin][before_resource_view] endpoint: {endpoint}")

            # Inicializamos listas de control en 'g' si no existen para esta petición HTTP
            if not hasattr(g, 'recursos_vistos'):
                g.recursos_vistos = []
            if not hasattr(g, 'recursos_descargados'):
                g.recursos_descargados = []

            # CASO A: El usuario está viendo la página del recurso
            if endpoint == 'dataset_resource.view':
                if resource_id not in g.recursos_vistos:
                    g.recursos_vistos.append(resource_id) # Candado para las múltiples ejecuciones de CKAN
                    
                    #log.info(f"[contador] ACCIÓN DETECTADA (ÚNICA): Carga de página real del recurso {resource_id}")
                    try:
                        helpers.guardar_contador(package_id, resource_id, 'View')
                    except Exception as e:
                        log.error(f"Error en contador de vistas: {str(e)}")

            # CASO B: El usuario está descargando el recurso directamente
            elif "/download" in path:
                if resource_id not in g.recursos_descargados:
                    g.recursos_descargados.append(resource_id) # Candado para las múltiples ejecuciones de CKAN
                    
                    #log.info(f"[contador] ACCIÓN DETECTADA (ÚNICA): Descarga real del recurso {resource_id}")
                    try:
                        # NOTA: Cambiado a 'Download' para diferenciar la acción en tu base de datos si aplica
                        helpers.guardar_contador(package_id, resource_id, 'Download')
                    except Exception as e:
                        log.error(f"Error en contador de descargas: {str(e)}")

        # Siempre debes retornar el diccionario original/modificado al final
        return res_dict

    def before_dataset_view(self, *args, **kwargs):
        #log.info("[ckanplugin] Entrando a before_dataset_view con *args")       
    
        # 1. Extraemos el data_dict de forma segura sin importar de dónde venga la llamada
        data_dict = None
        if len(args) > 1:
            data_dict = args[1]  # En package_search es (context, data_dict)
        elif len(args) == 1:
            data_dict = args[0]  # En la vista directa suele ser (data_dict)
        else:
            data_dict = kwargs.get('data_dict') or kwargs.get('package_dict')

        # Si no hay datos válidos, salimos devolviendo lo que llegó
        if not isinstance(data_dict, dict):
            return data_dict if data_dict else (args[-1] if args else None)

        # 3. Retornamos siempre el diccionario para que CKAN siga su flujo
        return data_dict


class CkanPlugin(CkanPluginLogin,CkanPluginPackageResourcePlugin):
    pass   