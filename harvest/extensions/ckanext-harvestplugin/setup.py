from setuptools import setup, find_packages

setup(
    name='ckanext-harvestplugin',
    version='0.1',
    description='Extension Para Diferentes Funciones',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points='''
        [ckan.plugins]  
        HarvestPlugin=ckanext.harvestplugin.plugin_logic:HarvestPlugin        
    ''',
)
