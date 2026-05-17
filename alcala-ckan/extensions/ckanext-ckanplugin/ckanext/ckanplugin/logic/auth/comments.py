import ckan.plugins.toolkit as tk
from ckan.plugins import toolkit
from sqlalchemy import func
from ckanext.ckanplugin.model.comments import Comments
import json, logging,os,  mimetypes

log = logging.getLogger(__name__)

def comments_set(context, data_dict):
    return {'success': True}

def comments_get(context, data_dict):
    return {'success': True}  