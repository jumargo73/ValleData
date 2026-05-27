import ckan.model as model
import ckan.plugins.toolkit as toolkit
import logging

log = logging.getLogger(__name__)


def reporte_federacion_global(options=None):
    '''
    Genera un listado consolidado de toda la data federada vÃ­a Harvest:
    Organizaciones, dependencias, datasets y metadatos de origen.
    '''
    log.warning("[HarvestPlugin][reporte_federacion_global] ejecutado")
    # 1. Definir los encabezados del CSV/JSON
    headers = [
        'Fuente Harvest (Nodo)', 
        'OrganizaciÃ³n ID', 
        'OrganizaciÃ³n (Nombre)', 
        'OrganizaciÃ³n (TÃ­tulo)', 
        'Dataset Name', 
        'Dataset Title', 
        'Num Recursos', 
        'Estado'
    ]
    
    # 2. Consulta SQL directa para optimizar el rendimiento con bases de datos grandes
    # Une las tablas de cosecha (harvest) con las tablas core de CKAN
    connection = model.Session.connection()
    query = """
        SELECT 
            hs.title AS fuente_harvest,
            g.id AS org_id,
            g.name AS org_name,
            g.title AS org_title,
            p.name AS dataset_name,
            p.title AS dataset_title,
            COUNT(r.id) AS num_recursos,
            p.state AS estado
        FROM package p
        INNER JOIN "group" g ON p.owner_org = g.id
        INNER JOIN harvest_object ho ON ho.package_id = p.id
        INNER JOIN harvest_source hs ON hs.id = ho.harvest_source_id
        LEFT JOIN resource r ON r.package_id = p.id
        WHERE p.state = 'active' 
          AND g.is_organization = true
        GROUP BY hs.title, g.id, g.name, g.title, p.name, p.title, p.state
        ORDER BY hs.title, g.title, p.title;
    """
    
    result = connection.execute(query)
    
    log.warning(f"[HarvestPlugin][reporte_federacion_global][result]:{result}")
    
    # 3. Construir la estructura 'table' como una lista de diccionarios
    table_data = []
    for row in result:
        table_data.append({
            'fuente_harvest': str(row['fuente_harvest'] or ''),
            'org_id': str(row['org_id'] or ''),
            'org_name': str(row['org_name'] or ''),
            'org_title': str(row['org_title'] or ''),
            'name': str(row['dataset_name'] or ''),      # Usado para la URL (slug)
            'title': str(row['dataset_title'] or ''),    # Usado para el texto del enlace
            'num_recursos': int(row['num_recursos'] or 0),
            'estado': str(row['estado'] or '')
        })
        
    # 4. Valores globales opcionales para la llave 'data'
    extra_data = {
        'total_datasets': len(table_data)
    }
    
            
    log.warning(f"[HarvestPlugin][reporte_federacion_global][table_data]:{table_data}")    
        
    # 4. Retornar el diccionario con la estructura requerida por ckanext-report
    return {
        'title': 'Reporte de Datos Federados (Harvest)',
        'description': 'Muestra el arbol completo de nodos origen, dependencias y datasets.',
        'table': table_data,
        'data': extra_data
    }
