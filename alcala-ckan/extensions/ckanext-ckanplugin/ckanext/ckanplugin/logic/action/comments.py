import ckan.plugins.toolkit as tk
from ckan.plugins import toolkit
from sqlalchemy import func
from ckan import model
from ckanext.ckanplugin.model.comments import Comments
import json, logging,os,  mimetypes
from ckan.common import _
import ckan.lib.i18n as ckan_i18n
from flask import request
from flask_babel import gettext as flask_gettext

log = logging.getLogger(__name__)

def comments_get(context, data_dict):

    dataset_id = None
    user_id=None

    try:

        # Si no se envía ninguno por defecto, usa el idioma base del contexto de CKAN
        idioma_solicitado = data_dict.get('lang', context.get('lang', 'es'))
        context['lang'] = idioma_solicitado
        ckan_i18n.set_lang(idioma_solicitado)
        log.warning(
                f"[Action][comments_get][idioma_solicitado]: {idioma_solicitado}"
            )

        
        
        # 1. Obtener los parámetros enviados en el data_dict
        dataset_id = data_dict.get('dataset_id')
        '''log.warning(
            f"[Action][comments_get] ejecutado id: {dataset_id}"
        )'''

        if not dataset_id:
            return {'success': False, 'error': 'Falta el dataset_id'}

        # 2. Consultar el último comentario ingresado para este dataset y este GUID
        query = model.Session.query(Comments).\
            filter(Comments.package_Id == dataset_id).\
            order_by(Comments.created.desc())

        ultimo_comentario = query.first()

        
        # 3. Validar si se encontró el registro
        if not ultimo_comentario:
            if idioma_solicitado == 'en':
                mensaje_final = 'No comments were found for this record'
            else:
                mensaje_final = 'No se encontraron comentarios para este registro.'
            
                return {
                    'success': False, 
                    'message':mensaje_final
                }

       
        # 4. Retornar el éxito junto con los datos del último comentario capturado
        return {
            'success': True,
            'comment': {
                'id': ultimo_comentario.id,
                'dataset_id': ultimo_comentario.package_Id,
                'user_guid': ultimo_comentario.user_id,
                'comment_text': ultimo_comentario.comment,
                'created': ultimo_comentario.created.strftime('%d/%m/%Y %H:%M')
            }
        }

    except Exception as e:
        log.error(
            f"[Action][comments_get] Error al guardar el comentario: {str(e)}"
        )

        if idioma_solicitado == 'en':
            mensaje_final = 'The user does not have permission to comment'
        else:
            mensaje_final = 'El usuario no tiene permisos para comentar.'

        return {
            'success': False, 
            'message':mensaje_final
        }    
    


def comments_set(context, data_dict):
    
    try:
        #log.warning("[action][resource_rating_set] ejecutado")
        tk.check_access('resource_rating_set', context, data_dict)

        resource_id = data_dict.get('dataset_id')
        comment = data_dict.get('comment_text')
        user_id = data_dict.get('user_id')
    
        #log.warning("[action][comments_set] resource_id %s",resource_id)
        #log.warning("[action][comments_set] rating %s",comment)
        #log.warning("[action][comments_set] user_id %s",user_id)

        if not resource_id:
            raise tk.ValidationError({'resource_id': 'Missing resource_id'})
            return {'success': False}

        if not comment:
            raise tk.ValidationError({'comment': 'Missing rating'})
            return {'success': False}

        else:    
        
            new_comments = Comments(
                package_Id=resource_id,
                user_id=user_id,          
                comment=comment,
            )

            #log.warning("[action][resource_rating_set][new_rating] %s",new_rating)
                    
            model.Session.add(new_comments)            

            resutl=model.Session.commit()
            #log.warning("[action][comments_set] store resutl %s",resutl)

            return {'success': True}
    except Exception as e:
        log.error(
            f"[Action][comments_set] Error al guardar el comentario: {str(e)}"
        )
        return {'success': False}