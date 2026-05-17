from setuptools import setup, find_packages,find_namespace_packages

setup(
    name='ckanext-harvestplugin',
    version='0.1',
    description='Extension Para Diferentes Funciones',
    
    # IMPORTANTE: Asegúrate de que find_packages() esté exactamente así:
    packages=find_namespace_packages(include=['ckanext.*']),
    include_package_data=True,    
    zip_safe=False,
    entry_points='''
        [ckan.plugins]  
        HarvestPlugin=ckanext.harvestplugin.plugin_logic:HarvestPlugin        
    ''',
)
