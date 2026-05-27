# -*- coding: utf-8 -*-
from setuptools import setup, find_packages,find_namespace_packages

setup(
    name='ckanext-harvestplugin',
    version='0.1',
    description='Extension Para Diferentes Funciones',
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    },      
    # IMPORTANTE: AsegÃÂºrate de que find_packages() estÃÂ© exactamente asÃÂ­:
    packages=find_namespace_packages(include=['ckanext.*']),
    include_package_data=True,    
    zip_safe=False,
    entry_points='''
        [ckan.plugins]  
        HarvestPlugin=ckanext.harvestplugin.plugin_logic:HarvestPlugin        
    ''',
)
