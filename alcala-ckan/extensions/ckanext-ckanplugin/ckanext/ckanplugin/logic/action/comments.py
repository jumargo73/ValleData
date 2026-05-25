import ckan.plugins.toolkit as tk
from ckan.plugins import toolkit
from sqlalchemy import func
from ckan import model
from ckanext.ckanplugin.model.comments import Comments
import json, logging,os,  mimetypes

log = logging.getLogger(__name__)

def comments_get(context, data_dict):

    dataset_id = None
    user_id=None

    try:

        
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

        '''log.warning(
            f"[Action][comments_get][ultimo_comentario]: {ultimo_comentario}"
        )'''

        # 3. Validar si se encontró el registro
        if not ultimo_comentario:
            return {
                'success': False, 
                'message': 'No se encontraron comentarios para este registro'
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
            f"[Action][resource_rating_get] Error al guardar la calificacion: {str(e)}"
        )
        return {
            'success': False,
            'message': 'El usuario no tiene permisos para comentar.' # <- Agrega esto
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