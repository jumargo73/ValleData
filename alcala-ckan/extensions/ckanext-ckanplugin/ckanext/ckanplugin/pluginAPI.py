from ckan.plugins import SingletonPlugin, implements,IPackageController, IResourceController
from ckan.plugins.interfaces import IConfigurer, IBlueprint
from ckan.plugins import toolkit
from ckan.common import config
import ckan.model as model
from ckan.model.resource import Resource  # ✅ Correcto import
from ckanext.ckanplugin.model.contador import Contador
from ckanext.ckanplugin.model.resourceRating import ResourceRating 
from model import Session
from flask import Blueprint, jsonify, redirect, request, Response
from ckan.types import Context 
from typing import Any
from sqlalchemy import func
from sqlalchemy.exc import ProgrammingError, OperationalError
from ckan.plugins.toolkit import ObjectNotFound, ValidationError



import logging, json, subprocess, os
from datetime import datetime


log = logging.getLogger(__name__)


class DataJsonView(SingletonPlugin):
    implements(IBlueprint)
    log.info("[DataJson] DataJson Cargado con Exito")

    def get_blueprint(self):

        bp = Blueprint('data_json', __name__)

        log.info("[DataJson][get_blueprint][data_json] ejecutado")


        @bp.route('/ckan/dashboard', methods=['GET'])
        def ckan_dashboard_stats():
            return toolkit.render('estadistica/dashboard.html')
        

        @bp.route('/api/3/action/data.json', methods=['GET'])
        def dataJson():

            log.info("[data_json][dataJson] ejecutado")
            context = {
                'model': model,
                'session': model.Session,
                'ignore_auth': True,
                'user': None
            }

            data={}
            try:

                # 1️⃣ Primero obtengo la cantidad total
                count_result = toolkit.get_action('package_search')(context, {
                    'rows': 0
                })
                registros = count_result['count']

                # 2️⃣ Ahora hago otra llamada trayendo exactamente esa cantidad
                responses = toolkit.get_action('package_search')(context, {
                    'rows': registros
                })



                package_responses=responses['results']

                log.warning(f"[DataJson] get_blueprint dataJson responses: {package_responses}")


                data={
                        "@context": "https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld",
                        "@type": "dcat:Catalog", 
                        "conformsTo": "https://project-open-data.cio.gov/v1.1/schema", 
                        "describedBy": "https://project-open-data.cio.gov/v1.1/schema/catalog.json",
                    }

                data['dataset']=[]

                url_site=config.get('ckan.site_url')


                count=0

                for package_response in package_responses:
                        

                    #log.warning(f"[DataJson] get_blueprint powerBI  {package_response['id']} posicion {count}') : {registros}")

                    if package_response.get('type', '').lower() != 'harvest':

                        grupos= package_response.get('groups')
                        organization=package_response.get('organization') 
                        tags=package_response.get('tags') 
                        resources=package_response.get('resources') 

                        if package_response.get('private')==True:
                            estado="Privado"
                        else:
                            estado="Público"

                        # 2. Invocas la función reutilizable para procesar las fechas                        
                        metadata_created=package_response.get('metadata_created')
                        log.info(f"[DataJson][package][metadata_created] : {metadata_created}") 
                        fecha_publicacion = self.formatear_fecha_ckan_a_iso(metadata_created)
                        log.info(f"[DataJson][package][fecha_publicacion] : {fecha_publicacion}")
                        
                        metadata_modified=package_response.get('metadata_modified')
                        log.info(f"[DataJson][package][metadata_modified] : {metadata_modified}") 
                        fecha_modificacion = self.formatear_fecha_ckan_a_iso(metadata_modified)    
                        log.info(f"[DataJson][package][fecha_modificacion] : {fecha_modificacion}") 

                        data_dataset={
                            "@type":"Dataset",
                            "identifier":package_response['id'], 
                            "landingPage":"{}".format(url_site+'/'+package_response.get('type')+'/'+package_response['id']),  
                            "title": package_response.get('title'),
                            "name": package_response.get('name'),
                            "description": package_response.get('notes'),
                            "dependencia":organization.get('title') if organization else '',
                            "issued": fecha_publicacion,
                            "modified": fecha_modificacion,
                            "ciudad": package_response.get('ciudad') or '' ,
                            "departamento":package_response.get('departamento') or '',
                            "accrualPeriodicity":package_response.get('frecuencia_actualizacion') or '',
                            "keywords":[tag["display_name"] for tag in tags],
                            "publisher":{
                                "@type": "org:Organization",
                                "name": "{}".format("org:"+ organization.get('title') if organization else ''),
                            },
                            "contactPoint":{
                                "@type": "vcard:Contact", 
                                "hasEmail": "mailto:datosabiertos@valledelcauca.gov.co", 
                                "fn":  "Valle Data"
                            },
                            "accessLevel":estado,
                            'license':{}                   
                        }


                        data_dataset['distribution']=[]
                        data_dataset['theme']=[]

                        if grupos:
                            data_dataset['theme'].append(grupos)

                        for resource in resources:

                            #fecha_publicacion = self.formatear_fecha_ckan_a_iso(resource.get['created'])
                            metadata_created=package_response.get('created')
                            log.info(f"[DataJson][package][metadata_created] : {metadata_created}") 
                            fecha_publicacion = self.formatear_fecha_ckan_a_iso(metadata_created)
                            log.info(f"[DataJson][package][fecha_publicacion] : {fecha_publicacion}")
                            
                            metadata_modified=package_response.get('metadata_modified')
                            log.info(f"[DataJson][package][metadata_modified] : {metadata_modified}") 
                            fecha_modificacion = self.formatear_fecha_ckan_a_iso(metadata_modified)    
                            log.info(f"[DataJson][package][fecha_modificacion] : {fecha_modificacion}") 

                            data_resource= {
                                "@type": "dcat:Distribution",
                                "description":resource.get('description') or '',
                                "downloadURL":resource.get('url') or '',  
                                "format":resource.get('format') or '',
                                "mediaType":resource.get('mediaType') or '',
                                "title":resource.get('name') or '',
                                "name": resource.get('name') or '',
                                "created": fecha_publicacion,   # <-- Creado del archivo
                                "last_modified": fecha_modificacion # <-- Modificado del archivo
                            }

                            data_dataset['distribution'].append(data_resource)
                    data['dataset'].append(data_dataset)
                return  jsonify(data) 
                #return Response(json.dumps(data), mimetype="application/json")

            except Exception as e:
                log.error(f"[DataJson] Error procesando get_blueprint data.json: {e}")   
                return jsonify({"success": False}) 



        

        @bp.route('/api/3/action/powerBI.json', methods=['GET'])
        def powerBI():

            """
            EndPoint para Tableros
            """
            log.info("[data_json][powerBI] ejecutado")
            context = {
                'model': model,
                'session': model.Session,
                'ignore_auth': True,
                'user': None
            }

            

            data={}
            try:

                # 1️⃣ Primero obtengo la cantidad total
                count_result = toolkit.get_action('package_search')(context, {
                    'rows': 0,
                    'include_private': True,
                    'fq': '+state:active'
                })
                registros = count_result['count']

                # 2️⃣ Ahora hago otra llamada trayendo exactamente esa cantidad
                responses = toolkit.get_action('package_search')(context, {
                    'rows': registros,
                    'include_private': True,
                    'fq': '+state:active'
                })
                

                package_responses=responses['results']

                #log.warning(f"[DataJson] get_blueprint powerBI context: {context}")

                #log.warning(f"[PluginApi][powerBI] responses: {package_responses}")

                #
                # log.warning(f"[DataJson] get_blueprint powerBI registros: {registros}")

                if package_responses:
                    
                    data={
                        "@context": "https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld",
                        "@type": "dcat:Catalog", 
                        "conformsTo": "https://project-open-data.cio.gov/v1.1/schema", 
                        "describedBy": "https://project-open-data.cio.gov/v1.1/schema/catalog.json",
                    }

                    data['conjuntoDatos']=[]
                    data['sellos']=[]

                    url_site=config.get('ckan.site_url')


                    count=0

                    
                    for package_response in package_responses:

                        #log.warning(f"[DataJson] get_blueprint powerBI  {package_response['id']} posicion {count}') : {registros}")

                        if package_response.get('type', '').lower() != 'harvest':

                            grupos= package_response.get('groups')
                            organization=package_response.get('organization') 
                            tags=package_response.get('tags') 
                            resources=package_response.get('resources') 

                            log.warning(f"[PluginApi][powerBI] resources: {resources}")

                            # Filtrar solo CSV con datastore activo
                            csv_resources = [
                                r for r in resources
                                if r.get("format", "").lower() == "csv"
                                and r.get("datastore_active")
                            ]

                            log.warning(f"[PluginApi][powerBI] csv_resources: {csv_resources}")

                            if not csv_resources:
                                continue


                            # Obtener el más reciente
                            latest_resource = max(
                                csv_resources,
                                key=lambda r: datetime.fromisoformat(r["created"])
                            )        
                            
                            log.warning(f"[PluginApi][powerBI] latest_resource: {latest_resource}")

                            estado=None    
                            if package_response.get('private')==True:
                                estado="Privado"
                            else:
                                estado="Público"

                            consolidado=package_response.get('consolidado')

                            #log.warning(f"[DataJson] get_blueprint powerBI organization: {organization}")

                            data_dataset={
                                "@type":"Dataset",
                                "identifier":package_response['id'], 
                                "landingPage":"{}".format(url_site+'/'+package_response.get('type')+'/'+package_response['id']),  
                                "title": package_response.get('title'),
                                "name": package_response.get('name'),
                                "description": package_response.get('notes'),
                                "dependencia":organization.get('title') if organization else '',
                                "issued": package_response.get('metadata_created') or '',
                                "modified": package_response.get('metadata_modified') or '',
                                "ciudad": package_response.get('ciudad') or '' ,
                                "departamento":package_response.get('departamento') or '',
                                "frecuencia_actualizacion":package_response.get('frecuencia_actualizacion') or '',
                                "keywords":[tag["display_name"] for tag in tags],
                                "publisher":{
                                    "@type": "org:Organization",
                                    "name": "{}".format("org:"+ organization.get('title') if organization else ''),
                                },
                                "contactPoint":{
                                    "@type": "vcard:Contact", 
                                    "hasEmail": "mailto:datosabiertos@valledelcauca.gov.co", 
                                    "fn":  "Valle Data"
                                },
                                "accessLevel":estado,
                                'licencia':{},
                                "Visualizaciones":consolidado.get('visualizaciones') if consolidado else 0,
                                "descargar":consolidado.get('descargas') if consolidado else 0,                                   
                            }

                            data_dataset['distribucion']=[]
                            data_dataset['tema']=[]
                            

                            contador=latest_resource.get('contador') 
                            #log.warning(f"[PliginApi][powerBI] contador: {contador}")
                            estructura=latest_resource.get('estructura') 
                            #log.warning(f"[PliginApi][powerBI] estructura: {estructura}")
                            data_extras=latest_resource.get('data_extra')    
                            #log.warning(f"[PliginApi][powerBI] data_extras: {data_extras}")
                            calificacion=latest_resource.get('calificacion')
                            
                            data_dataset['calificacion']=calificacion['average'] if calificacion else 0

                            data_resource= {
                                "@type": "dcat:Distribution",
                                "description":latest_resource['description'] or '',
                                "downloadURL":latest_resource['url'] or '',  
                                "format":latest_resource['format'] or '',
                                "mediaType":latest_resource['mimetype'] or '',
                                "title":latest_resource.get('name') or '',
                                "name": latest_resource.get('name') or '',
                                "issued": latest_resource['created'].strftime("%Y-%m-%dT%H:%M:%SZ") or '',
                                "modified": latest_resource['last_modified'].strftime("%Y-%m-%dT%H:%M:%SZ") or '',                              
                                "filas":estructura['filas'] if estructura else 0 ,
                                "columnas":estructura['columnas'] if estructura else 0 ,
                                "vistas":contador['visualizaciones'] if contador else 0,
                                'descargas':contador['descargas'] if contador else 0,
                            }


                            if grupos:
                                data_dataset['tema'].append(grupos)
                           
                           
                                        #nombre_resource=resource.get('name')
                            data_dataset['distribucion'].append(data_resource)

                               

                            #log.warning(f"[DataJson] get_blueprint powerBI resources_response: {resource}")

                        #log.warning(f"[DataJson] get_blueprint powerBI data_dataset: {data_dataset}")
                        data['conjuntoDatos'].append(data_dataset)

                        #log.warning(f"[DataJson] get_blueprint powerBI data_dataset: {data_dataset}")

                        count+=1
                            
                return  jsonify(data) 
                #return Response(json.dumps(data), mimetype="application/json")

            except Exception as e:
                log.error(f"[PluginApi][powerBI] Error procesando powerBi.json {e}")
                return jsonify({"success": False})


        @bp.route('/api/3/action/dataset_huerfanos', methods=['GET'])        
        def dataset_huerfanos():
            log.info("[data_json][dataset_huerfanos] ejecutado")
             
            context = {'model': model, 'session': model.Session, 'ignore_auth': True, 'user': 'opendata'}

            count_result = toolkit.get_action('package_search')(context, {
                    'rows': 0,
                    'include_private': True,
                    'fq': '+state:active'
                })
            registros = count_result['count']

            # 1. Obtener datasets sin grupo
            res_sin_grupo = toolkit.get_action('package_search')(context, {
                'q': '*:*',
                'fq': 'state:active AND -groups:[* TO *]',
                'rows': registros,
                'include_private': True
            })

            # 2. Obtener datasets sin organización
            res_sin_org = toolkit.get_action('package_search')(context, {
                'q': '*:*',
                'fq': 'state:active AND -owner_org:[* TO *]',
                'rows': registros,
                'include_private': True
            })

            # 3. Unir y eliminar duplicados usando el ID único
            # Usamos un diccionario para mantener el objeto completo pero evitar IDs repetidos
            unificados = {ds['id']: ds for ds in (res_sin_grupo['results'] + res_sin_org['results'])}

            # Retornamos la lista final
            return jsonify(list(unificados.values()))

       

        @bp.route('/api/3/action/dashboard_stats', methods=['GET'])        
        def dashboard_stats():

            log.info("[data_json][dashboard_stats] ejecutado")
            

            # Usamos ignore_auth para que el dashboard sea público pero vea todo
            context = {
                'model': model,
                'session': model.Session,
                'ignore_auth': True,
                'user': 'opendata'
            }


            count_result = toolkit.get_action('package_search')(context, {
                    'rows': 0,
                    'include_private': True,
                    'fq': '+state:active'
                })
            registros = count_result['count']

            # 2️⃣ Ahora hago otra llamada trayendo exactamente esa cantidad
            privados = self.contar_privados(context,registros)       
                     
            
            # 2. Huérfanos (tu consulta favorita)
            huerfanos = self.obtener_huerfanos_totales(context,registros)  

            #formatos
            formatos_raw = self.get_stats_formatos(context,registros)   

            grupos_raw=self.get_stats_grupos(context,registros)        
          
            organizacion_raw=self.obtener_organizacion_facet(context,registros) 
            # ... (tus conteos de datasets, huérfanos y privados anteriores) ...

            stats_tematicas=self.get_stats_tematicas(context,registros) 

            consolidado_contador_organizaciones=self.get_consolidado_contador_organizaciones(context,registros)
            consolidado_contador_grupos=self.get_consolidado_contador_grupos(context,registros)
            consolidado_contador_dataset=self.get_consolidado_contador_dataset(context,registros)
            # 4. Total de Organizaciones
            orgs = toolkit.get_action('organization_list')(context, {})
            total_orgs = len(orgs)

            # 5. Total de Grupos
            grupos = toolkit.get_action('group_list')(context, {})
            total_grupos = len(grupos)

            data=jsonify({
                'total_datasets': registros,
                'huerfanos': huerfanos,
                'privados': privados,
                'total_orgs': total_orgs,
                'total_grupos': total_grupos,
                'formatos_raw':formatos_raw,
                'grupos_raw' : grupos_raw,
                'organizacion_raw':organizacion_raw,
                'stats_tematicas':stats_tematicas,
                'consolidado_contador_grupos':consolidado_contador_grupos,
                'consolidado_contador_organizaciones':consolidado_contador_organizaciones,
                'consolidado_contador_dataset':consolidado_contador_dataset
            })    
            log.warning(f"[DataJson[dashboard_stats][data]={data}")

            return data
            
        return bp 

    def obtener_organizacion_facet(self,context:Context,registros):
        # 'ignore_auth': True es lo que permite ver los privados sin restricciones
        
        data_dict = {
            'q': '*:*',
            'include_private': True,
            'rows': registros,
            'facet': True,
            'facet.field': ['organization']
        }
        
        resultado = toolkit.get_action('package_search')(context, data_dict)

        organizacion_raw = resultado.get('search_facets', {}).get('organization', {}).get('items', [])
        
        organizacion_limpios = {f['name']: f['count'] for f in organizacion_raw}

        organizacion_limpios['Total_Datasets']=resultado['count']

        log.warning(f"[DataJson[dashboard_stats][grupos_raw][data]={organizacion_limpios}")

        return organizacion_limpios    
    

    def get_stats_grupos(self,context:Context,registros):
        # 'ignore_auth': True es lo que permite ver los privados sin restricciones
        
        data_dict = {
            'q': '*:*',
            'include_private': True,
            'rows': registros,
            'facet': True,
            'facet.field': ['groups']
        }
        
        resultado = toolkit.get_action('package_search')(context, data_dict)

        grupos_raw = resultado.get('search_facets', {}).get('groups', {}).get('items', [])
        
        grupos_limpios = {f['name']: f['count'] for f in grupos_raw}

        grupos_limpios['Total_Datasets']=resultado['count']

        log.warning(f"[DataJson[dashboard_stats][grupos_raw][data]={grupos_limpios}")

        return grupos_limpios

    def obtener_huerfanos_totales(self,context:Context,registros):
        # 'ignore_auth': True es lo que permite ver los privados sin restricciones
        log.info("[data_json][obtener_huerfanos_totales] ejecutado")

        context = {'model': model, 'session': model.Session, 'ignore_auth': True, 'user': 'opendata'}

        count_result = toolkit.get_action('package_search')(context, {
                'rows': 0,
                'include_private': True,
                'fq': '+state:active'
            })
        registros = count_result['count']

        # 1. Obtener datasets sin grupo
        res_sin_grupo = toolkit.get_action('package_search')(context, {
            'q': '*:*',
            'fq': 'state:active AND -groups:[* TO *]',
            'rows': registros,
            'include_private': True
        })

        # 2. Obtener datasets sin organización
        res_sin_org = toolkit.get_action('package_search')(context, {
            'q': '*:*',
            'fq': 'state:active AND -owner_org:[* TO *]',
            'rows': registros,
            'include_private': True
        })

        # 3. Unir y eliminar duplicados usando el ID único
        # Usamos un diccionario para mantener el objeto completo pero evitar IDs repetidos
        unificados = {ds['id']: ds for ds in (res_sin_grupo['results'] + res_sin_org['results'])}

        # Retornamos la lista final
        data=list(unificados.values())
        
        return len(data)    

    
    def contar_privados(self,context:Context,registros):
        # Es vital usar ignore_auth para que el conteo sea real (vea todo)
            
        data_dict = {
            'q': '*:*',
            'fq': 'capacity:private', # Filtramos solo por capacidad privada
            'rows': registros,                 # No queremos la lista, solo el total
            'include_private': True,
            'facet.limit': -1,
            'facet.mincount': 1
        }
        
        resultado = toolkit.get_action('package_search')(context, data_dict)
        log.warning(f"[DataJson[dashboard_stats][contar_privados][resultado]={resultado}")
        return resultado['count']
    
    def get_stats_formatos(self,context:Context,registros):
        search_params = {
            'q': '*:*',
            'rows': 1000,
            'include_private': True,  # Trae públicos y privados
            'fq': 'state:active'      # Solo activos
        }
        
        results = toolkit.get_action('package_search')(context, search_params)
        stats_formatos = {}
        total_recursos=0

        for dataset in results.get('results', []):
            # Extraemos los recursos de cada dataset (sea público o privado)
            resources = dataset.get('resources', [])
            
            for res in resources:
                if res.get('state') == 'active':
                    # Normalizamos el formato (ej: 'csv', 'CSV', 'text/csv' -> 'CSV')
                    formato = res.get('format', 'Desconocido').upper().strip()
                    
                    if not formato:
                        formato = "S/F" # Sin Formato

                    if formato not in stats_formatos:
                        stats_formatos[formato] = 0
                    
                    stats_formatos[formato] += 1
                total_recursos+= 1
        # Convertimos a una lista de objetos para Angular
        formatos_json = [
            {'nombre': k, 'cantidad': v} 
            for k, v in stats_formatos.items()
        ]

        
        total_recursos={'nombre': 'total_recursos', 'cantidad': total_recursos}
        formatos_json.append(total_recursos)
        log.info(f"[DataJson][[dashboard_stats]][get_stats_formatos][total_recursos]={total_recursos}")
        
        # Ordenamos de mayor a menor
        formatos_json.sort(key=lambda x: x['cantidad'], reverse=True)
        
        return formatos_json

    def get_stats_tematicas(self,context:Context,registros):
        # 1. Obtenemos todos los datasets (ajusta 'rows' según tu volumen)
        search_params = {
            'q': '*:*',
            'rows': registros,
            'include_private': True,
            'fq': '+state:active'
        }
        results = toolkit.get_action('package_search')(context, search_params)
        log.info("[data_json][get_stats_tematicas][results]",results)
        
        stats = {}

        stats = {}

        for dataset in results.get('results', []):
            groups = dataset.get('groups', [])
            
            # --- AQUÍ ESTÁ EL TRUCO ---
            # Si la lista de grupos está vacía, saltamos al siguiente dataset inmediatamente
            if not groups:
                log.info("Saliendo de este dataset: No tiene temáticas asignadas.")
                continue 

            # 2. CONTEO MANUAL (La verdad absoluta)
            # En lugar de usar dataset.get('num_resources'), contamos los recursos activos
            recursos_activos = [
                res for res in dataset.get('resources', []) 
                if res.get('state') == 'active'
            ]
            conteo_real = len(recursos_activos)

            log.info(f"Dataset: {dataset.get('name')} | Estado: {dataset.get('capacity')} | Recursos Activos: {conteo_real}")

            for group in groups:
                group_name = group.get('name')
                if group_name not in stats:
                    stats[group_name] = {
                        'titulo': group.get('title') or group.get('display_name'),
                        'total_datasets': 0,
                        'total_recursos': 0,
                        'url_ver_mas': f'/group/{group_name}'
                    }
                
                # Solo sumará si el dataset pasó el 'if not groups'
                stats[group_name]['total_datasets'] += 1
                stats[group_name]['total_recursos'] += conteo_real

        # Convertimos el diccionario a una lista para que el JSON sea más fácil de recorrer en Angular
        return list(stats.values())
    
    def get_consolidado_contador_organizaciones(self,context:Context,registros):

        resultados_totales = []
        
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user  # o el nombre de un usuario válido
        }   

        
        data_dict = {
            'all_fields': True,   # Si quieres que traiga más datos
            'include_extras': True
        } 

        orgs = toolkit.get_action('organization_list')(context, data_dict)

        log.info(f"[DataJsonView][get_consolidado_contador_organizaciones] orgs: {orgs}")
        
        for org in orgs:

            busqueda_params = {
                'q': '*:*',
                'rows': registros,
                'include_private': True,
                'fq': f'+state:active AND owner_org:{org["id"]}'
            }

            log.info(f"[DataJsonView][get_consolidado_contador_organizaciones]  busqueda_params: { busqueda_params}")
              
            datasets = toolkit.get_action('package_search')(context,busqueda_params)
            log.info(f"[DataJsonView][get_consolidado_contador_organizaciones] packages: {datasets['results']}")
            resultados_totales.append(self.consolidado_contador(datasets['results'],org["name"],None))
           
        log.info(f"[DataJsonView][get_consolidado_contador_organizaciones] resultados_totales: {resultados_totales}")    
        return resultados_totales
    

    def get_consolidado_contador_grupos(self,context:Context,registros):

        resultados_totales = []
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user  # o el nombre de un usuario válido
        }

      
        data_dict = {
            'all_fields': True,   # Si quieres que traiga más datos
            'include_extras': True
        }

        groups = toolkit.get_action('group_list')(context, data_dict)
        log.info(f"[DataJsonView][get_consolidado_contador_grupos] groups: {groups}")

        for group in groups:

            busqueda_params = {
                'q': '*:*',
                'rows': registros,
                'include_private': True,
                'fq': f'+state:active AND groups:{group["name"]}'
            }

            log.info(f"[DataJsonView][get_consolidado_contador_grupos]  busqueda_params: { busqueda_params}")  
            datasets = toolkit.get_action('package_search')(context,busqueda_params)
            log.info(f"[DataJsonView][get_consolidado_contador_grupos] packages: {datasets['results']}")
            resultados_totales.append(self.consolidado_contador(datasets['results'],None,group["name"]))
           
        log.info(f"[DataJsonView][get_consolidado_contador_grupos] resultados_totales: {resultados_totales}")    
        return resultados_totales
    

    def get_consolidado_contador_dataset(self,context:Context,registros):

        resultados_totales = []
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user  # o el nombre de un usuario válido
        }


        data_dict = {
            'q': '*:*',
            'rows': registros,
            'include_private': True,
            'fq':'+state:active'
        }

        resultado = toolkit.get_action('package_search')(context, data_dict)
        datasets = resultado.get('results', [])
        log.info(f"[get_consolidado_contador_dataset] dataset: {datasets}")

        for dataset in datasets:
            log.info(f"[DataJsonView][get_consolidado_contador_dataset] packages: {dataset}")
            log.info(f"[DataJsonView][get_consolidado_contador_dataset] packages: {dataset['id']}-{dataset['name']}")
            resultados_totales.append(self.get_consolidado_contador(dataset['id'],dataset['name']))
           

        return resultados_totales
      

    def consolidado_contador(self,packages, org_id=None,group_id=None):
        """
            Devuelve el consolidado de las vistas y descargas de los recursos.
        """

        log.info("[DataJsonView][consolidado_contador] ejecutado")
    
       
        vistas=0
        descargas=0

        log.info(f"[DataJsonView][consolidado_contador] packages: {packages}")



        #datasets=packages['results']

        for package in  packages:
            log.info(f"[consolidado_contador] package: {package}")
            package_id=package['id']
            rows = Session.query(Contador).filter(
                    Contador.package_Id == package_id
                ).all()

            log.info(f"[DataJsonView][consolidado_contador] contadores {rows} en Dataset {package_id}")
        
            for row in rows:
                vistas+=row.contVistas
                descargas+=row.contDownload
            
        log.info(f"[DataJsonView][consolidado_contador] vistas {vistas} descargas {descargas}")
        
        if org_id==None:

            return{
                    "visualizaciones": vistas if vistas else 0,
                    "descargas": descargas if descargas else 0,
                    "group_id": group_id,
                }
    
        else:
            return{
                    "visualizaciones": vistas if vistas else 0,
                    "descargas": descargas if descargas else 0,
                    "org_id": org_id,
                }  


    def formatear_fecha_ckan_a_iso(self,fecha_raw):
        """
        Convierte cualquier marca de tiempo de la base de datos de CKAN
        al formato estricto ISO 8601 con zona horaria UTC (Z) exigido por DCAT.
        
        Parámetros:
        fecha_raw (str/datetime): La fecha cruda proveniente de CKAN.
        
        Retorna:
        str: Cadena de texto formateada como 'YYYY-MM-DDTHH:mm:ssZ'.
            Si ocurre un error o la fecha es inválida, retorna la fecha actual.
        """
        log.info("[DataJsonView][formatear_fecha_ckan_a_iso] ejecutado")  
        log.info(f"[DataJsonView][formatear_fecha_ckan_a_iso][fecha_raw]={fecha_raw}")  
        if not fecha_raw:
            # Fallback de seguridad: si no hay fecha, usa el tiempo actual
            return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            
        # Si ya es un objeto datetime, lo convertimos a string formateado directamente
        if isinstance(fecha_raw, datetime):
            return fecha_raw.strftime("%Y-%m-%dT%H:%M:%SZ")
            
        # Si llega como texto, limpiamos espacios y caracteres inválidos
        fecha_str = str(fecha_raw).strip().replace(" ", "T")
        
        # Lista de formatos comunes que CKAN guarda en su base de datos
        formatos_compatibles = [
            "%Y-%m-%dT%H:%M:%S.%f",  # Con microsegundos (2026-05-07T15:25:36.827197)
            "%Y-%m-%d %H:%M:%S.%f",  # Con espacio y microsegundos
            "%Y-%m-%dT%H:%M:%S",     # Estándar sin decimales
            "%Y-%m-%d %H:%M:%S"      # Con espacio sin decimales
        ]
        
        for formato in formatos_compatibles:
            try:
                # Reemplazamos la T si el formato actual de la lista usa espacio
                fmt_limpio = formato.replace(" ", "T")
                objeto_dt = datetime.strptime(fecha_str, fmt_limpio)
                # Retorna el formato ISO exacto con la Z concatenada y sin microsegundos
                return objeto_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                continue
                
        # Si ningún formato coincide, aplicamos recorte seguro de texto como último recurso
        try:
            return fecha_str[:19].replace(" ", "T") + "Z"
        except Exception:
            # Si todo lo demás falla, retorna la fecha de hoy para no romper la cosecha
            return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            
    

   
        

class DataJsonAPI(SingletonPlugin):
    implements(IPackageController)
    implements(IResourceController)

    #Eventos Resource

    def before_resource_create(self,context: Context, resource: dict[str, Any]):
        pass

    def after_resource_create(self,context: Context, resource: dict[str, Any]):
        pass

    def before_resource_update(self,context: Context, current: dict[str, Any], resource: dict[str, Any]):
        pass

    def after_resource_update(self, context, resource):
        pass        
        
     
   
    def before_resource_delete(self,context: Context, resource: dict[str, Any], resources: list[dict[str, Any]]):
        pass

    def after_resource_delete(self,context: Context, resources: list[dict[str, Any]]):
        pass

    def before_resource_show(self,resource_dict: dict[str, Any]):
        return resource_dict

    def before_resource_search(self,search_params: dict[str, Any]):
        return search_params  

    def after_resource_search(self,context: Context,data_dict: dict[str, Any], search_params: dict[str, Any]):
        return data_dict 


    #Eventos Dataset
    
    def after_dataset_update(self, context: Context, data_dict: dict[str, Any]):
        # Tu lógica aquí
        return data_dict

    def after_dataset_create(self,context: Context,  pkg_dict: dict[str, Any]):        
        return pkg_dict  

    def after_dataset_delete(self,context: Context, pkg_dict: dict[str, Any]):
        pass

    def before_dataset_show(self,context: Context, pkg_dict: dict[str, Any]):
        return pkg_dict

    def after_dataset_show(self,context: Context, pkg_dict: dict[str, Any]):    
        return pkg_dict
        
    def before_dataset_view(self,pkg_dict: dict[str, Any]):
        return pkg_dict  
        
    # --- dataset_search ---    
    def before_dataset_search(self,search_params: dict[str, Any]):
        return search_params           
    

    def after_dataset_search(self,search_results: dict[str, Any], search_params: dict[str, Any]):
        try:

            contadores=[]            
            
            # 1️⃣ Obtener contadores desde tu acción
            #contador_action = toolkit get_action('contador_get')
            context = {
                'model': model,
                'session': model.Session,
                'user':  toolkit.g.user or  toolkit.config.get('ckan.site_id')
            }

            log.info(f"[DataJsonAPI][after_dataset_search] context {context}")
            
            contadores = self.contador_get()
            
            
            log.info(f"[DataJsonAPI][after_dataset_search] contadores {contadores}")

            # 2️⃣ Optimizar acceso mapeando por resource_id
            contador_map = {c['resource_id']: c for c in contadores}

            # 3️⃣ Iterar los datasets y agregar contador a cada recurso
            for dataset in search_results.get('results', []):

                package_id=dataset.get('id') if dataset else ''

                consolidado=self.get_consolidado_contador(package_id)
                calificacion=self.get_calificacion_dataset(package_id)

                dataset['consolidado']=consolidado if consolidado else {}
               

                log.info(f"[DataJsonAPI] after_dataset_search package['id']= {package_id} consolidado {consolidado}")
                for resource in dataset.get('resources', []):
                    #log.info(f"[DataJsonAPI] after_dataset_search resource['id']= {resource['id']}")
                    rid = resource.get('id')
                    filas_columnas_map=self.get_filas_columnas(rid,context)
                    data_extra=self.get_extras(rid)
                    resource['contador'] = contador_map.get(rid, None)
                    resource["estructura"] = filas_columnas_map
                    resource["data_extra"] =data_extra
                    resource["calificacion"] =calificacion

        except Exception as e:
            log.error(
                f"[DataJsonAPI] Error after_dataset_search: {str(e)}"
            )

        return search_results
          

    def before_dataset_index(self,pkg_dict: dict[str, Any]):
        return pkg_dict    
    
    # --- create ---   
    def create(self,entity: model.Package):
        pass
    
    # --- delete ---  
    def delete(self,entity: model.Package):
        pass
    
    # --- create ---
    def edit(self,entity: model.Package):
        pass        
        
    # --- READ ---      
    def read(self,entity: model.Package):
        pass

    def contador_get(self):
        """
        Devuelve los contadores almacenados en la tabla personalizada.
        """

        #log.info("[DataJsonAPI] contador_get ejecutado")
    
        session = model.Session

        rows = session.query(Contador).all()

        log.info(f"[DataJsonAPI][contador_get] registro {rows}")

        return [
            {
                "source_Id": row.source_Id,
                "contVistas": row.contVistas,
                "contDownload": row.contDownload,
                "package_Id": row.package_Id,
            }
            for row in rows
        ]  
    
    def get_consolidado_contador(self,package_id): 
                
        """
            Devuelve el consolidado de las vistas y descargas de los recursos.
        """

        log.info("[DataJsonAPI] get_consolidado_contador ejecutado")
    
        session = model.Session

        vistas=0
        descargas=0

        rows = Session.query(Contador).filter(
                Contador.package_Id == package_id
            ).all()

       
        for row in rows:
            vistas+=row.contVistas
            descargas+=row.contDownload
            log.info(f"[DataJsonAPI][get_consolidado_contador] vistas {vistas} descargas {descargas}")

        
        log.info(f"[DataJsonAPI][get_consolidado_contador] registro {rows}")

        return{
                "visualizaciones": vistas if vistas else 0,
                "descargas": descargas if descargas else 0,
                "package_id": package_id,
            }
    
    

    def get_extras(self,id):

        
        try:

            #log.info("[DataJsonAPI] get_extras ejecutado")

            resource_model = Session.query(Resource).filter(
                Resource.format.ilike('PDF'),
                Resource.id == id
            ).first()

            if not resource_model:
                #log.warning("[DataJson] get_extras No se encontró recurso con ID: %s", id)
                return {
                    "resource_id":id,
                    "categoria":"",
                    "fecha_obtencion":"",
                    "fecha_vencimiento":"",
                    "dependiencia":"",
                    "nivel":"",
                }  

            extras = {}

            if resource_model.extras:
                if isinstance(resource_model.extras, str):
                    try:
                        extras = json.loads(resource_model.extras)
                    except Exception as e1:
                            log.error(f"[DataJson] Error id {id} {e1}")
                            return {
                                "resource_id":id,
                                "categoria":"",
                                "fecha_obtencion":"",
                                "fecha_vencimiento":"",
                                "dependiencia":"",
                                "nivel":"",
                                "error": str(e1)
                            }  
                elif isinstance(resource_model.extras, dict):
                    extras = resource_model.extras

            if extras.get('type')=="sello_excelencia":
                return {
                    "resource_id":id,
                    "categoria":extras.get('type'),
                    "fecha_obtencion":extras.get('fecha_obtencion'),
                    "fecha_vencimiento":extras.get('fecha_vencimiento'),
                    "dependiencia":extras.get('owner_org'),
                    "nivel":extras.get('nivel'),
                    "error": ""
                }        
            else:
                return {
                    "resource_id": id,
                    "categoria":"",
                    "fecha_obtencion":"",
                    "fecha_vencimiento":"",
                    "dependiencia":"",
                    "nivel":"",
                    "error": "No tiene Sello de Excelencia"
                }  
        
        except Exception as e:
            log.error(f"[DataJson] Error id {id} {e}")
            return [
                {
                    "resource_id":id,
                    "categoria":"",
                    "fecha_obtencion":"",
                    "fecha_vencimiento":"",
                    "dependiencia":"",
                    "nivel":"",
                    "error":str(e)
                }
            ]


    def get_calificacion_dataset(self,id):
        try:
            log.warning("[DataJsonAPI][get_calificacion_dataset] ejecutado")

            log.warning("[DataJsonAPI][get_calificacion_dataset][package] %s",id) 
            existing = model.Session.query(ResourceRating).filter_by(
                package_Id=id
            ).first()
            
            log.warning("[DataJsonAPI][get_calificacion_dataset][existing] %s",existing)
            if existing:
                
                result = model.Session.query(
                    func.avg(ResourceRating.ratings),
                    func.count(ResourceRating.id)
                ).filter_by(package_Id=id).first()

                log.warning("[DataJsonAPI][get_calificacion_dataset][result]= %s",result)
                average = result[0] or 0
                count = result[1]

                data=  {
                    'resource_id': id,
                    'average': float(round(average, 2)),
                    'count': count,
                    'user-rating':existing.ratings
                }

                #log.warning("[action][resource_rating_get] average=%s",float(round(average, 2)))
                #log.warning("[action][resource_rating_get] count=%s",count)
                log.warning(f"[DataJsonAPI][get_calificacion_dataset][rating]= {data}")

                return data

            else:
                return {
                    'resource_id': id,
                    'average': 0.0,
                    'count': 0,
                    'user-rating':None
                }     
            
        except Exception as e:
            log.error(f"[DataJsonAPI][get_calificacion_dataset][error]= {e}")
            return {
                'resource_id': id,
                'average': 0.0,
                'count': 0,
                'user-rating':None
            }
            
    def get_filas_columnas(self,id,context):
        try:
            #log.info("[DataJsonAPI] get_filas_columnas ejecutado")
            datastore_response =  toolkit.get_action('datastore_search')(context,{'id': id})
            if datastore_response:
                columnas = len(datastore_response.get("fields", []))
                filas = datastore_response.get("total", 0)  
                #log.warning(f"[DataJsonAPI] get_filas_columnas con id={id}: filas={filas}, columnas={columnas}")
                return{
                        "resource_id": id,
                        "filas": filas,
                        "columnas": columnas,
                        "error": ""
                    }
                
                
            else:
                #log.warning(f"[DataJsonAPI] get_filas_columnas con id={id}: filas=0,columnas=0")
                return {
                        "resource_id": id,
                        "filas": 0,
                        "columnas": 0,
                        "error": str(datastore_response)
                    }
                
               

        except (ProgrammingError, OperationalError, ObjectNotFound, ValidationError, Exception) as e:
            log.warning(f"[CkanPlugin][datastore_search] No se pudo consultar el DataStore para el recurso {id}. Tabla inexistente o ID no cargado. Error original: {str(e)}")
            return {
                    "resource_id": id,
                    "filas": 0,
                    "columnas": 0,
                    "error": str(e)
                }

    

    
class DataJsonPlugin(DataJsonView,DataJsonAPI):
    pass    