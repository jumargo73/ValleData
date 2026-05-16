import ckan.plugins as p
from ckan.plugins import toolkit
from flask import Blueprint
import logging

log = logging.getLogger(__name__)
class CkanAngularPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer ,inherit=True)
    p.implements(p.IBlueprint)

    # IConfigurer: Registra carpetas
    def update_config(self, config):
        log.warning("[CkanAngularPlugin][update_config] ejecutado")
        if not getattr(config, '_ckanangular_loaded', False):
            toolkit.add_template_directory(config, 'templates')
            toolkit.add_public_directory(config, 'public')
            toolkit.add_resource('public','ckanext-ckanangular')
            config._ckanangular_loaded = True

    # IBlueprint: Crea la URL para ver la app
    def get_blueprint(self):
         # Blueprint 2
        angular_bp = Blueprint("angular_bp", __name__)        
        
        angular_bp.add_url_rule('/angular', view_func=self.hello_angular)
        return angular_bp

    def hello_angular(self):
        return toolkit.render('/home/index_angular.html')
