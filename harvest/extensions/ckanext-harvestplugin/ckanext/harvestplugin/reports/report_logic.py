import ckan.model as model
import logging

log = logging.getLogger(__name__)

def reporte_federacion_global(options=None):
    
    log.warning("[HarvestPlugin][reporte_federacion_global] ejecutado")  
    headers = ['Fuente', 'Org ID', 'Org Name', 'Org Title', 'Name', 'Title', 'Recursos', 'Estado']
    
    connection = model.Session.connection()
    query = """
        SELECT 
            hs.title AS fuente_harvest, g.id AS org_id, g.name AS org_name, g.title AS org_title,
            p.name AS dataset_name, p.title AS dataset_title, COUNT(r.id) AS num_recursos, p.state AS estado
        FROM package p
        INNER JOIN "group" g ON p.owner_org = g.id
        INNER JOIN harvest_object ho ON ho.package_id = p.id
        INNER JOIN harvest_source hs ON hs.id = ho.harvest_source_id
        LEFT JOIN resource r ON r.package_id = p.id
        WHERE p.state = 'active' AND g.is_organization = true
        GROUP BY hs.title, g.id, g.name, g.title, p.name, p.title, p.state;
    """
    result = connection.execute(query)
    
    table_data = []
    org_counts = {}  # Para el gráfico de barras
    total_recursos = 0
    
    
    for row in result:
        num_res = int(row['num_recursos'] or 0)
        total_recursos += num_res
        
        # Agrupar conteos para el gráfico
        org_tit = str(row['org_title'] or 'Sin Organización')
        org_counts[org_tit] = org_counts.get(org_tit, 0) + 1
        
        table_data.append({
            'fuente_harvest': str(row['fuente_harvest'] or ''),
            'org_id': str(row['org_id'] or ''),
            'org_name': str(row['org_name'] or ''),
            'org_title': org_tit,
            'name': str(row['dataset_name'] or ''),
            'title': str(row['dataset_title'] or ''),
            'num_recursos': num_res,
            'estado': str(row['estado'] or '')
        })
        
    # Variables de control macro para el Dashboard
    extra_data = {
        'total_datasets': len(table_data),
        'total_recursos': total_recursos,
        'total_organizaciones': len(org_counts),
        'grafico_organizaciones': list(org_counts.keys()),
        'grafico_valores': list(org_counts.values())
    }
    
    respuesta = {
        'title': 'Tablero de Control de la Federación de Datos',
        'description': 'Métricas analíticas en tiempo real de los nodos y dependencias cosechadas.',
        'table': table_data,
        'metricas': extra_data
    }
    
    log.warning(f"[HarvestPlugin][reporte_federacion_global][respuesta]:{respuesta}")   
        
    return respuesta
