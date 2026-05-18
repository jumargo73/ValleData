from sqlalchemy import Column, UnicodeText, Integer, ForeignKey,String,UniqueConstraint
from ckan.model.types import make_uuid
try:
    from ckan.plugins.toolkit import BaseModel
except ImportError:
    # CKAN <= 2.9
    from ckan.model.meta import metadata
    from sqlalchemy.ext.declarative import declarative_base
    BaseModel = declarative_base(metadata=metadata)

import json, logging,os,  mimetypes

log = logging.getLogger(__name__)

class ResourceRating(BaseModel):

    __tablename__ = 'resource_rating'

    id = Column(Integer, primary_key=True,autoincrement=True)
    package_Id = Column(String, nullable=False)
    ratings = Column(Integer, nullable=False,default=0)
    user_id = Column(String, nullable=False,default=0)

    __table_args__ = (
        UniqueConstraint('package_Id',name='uix_source_package'),
    )

    def __init__(self,  package_Id=None,user_id=None,ratings=None, **kwargs ):
        super().__init__(**kwargs)
        self.package_Id = package_Id
        self.user_id = user_id
        self.ratings = ratings
       

        #log.warning("[Model][ResourceRating][__init__] package_Id %s",self.package_Id)
        #log.warning("[Model][ResourceRating][__init__] user_id %s",self.user_id)
        #log.warning("[Model][ResourceRating][__init__] ratings %s",self.ratings)
        
        # Garantizar valores por defecto si no vienen
        self.calificate = kwargs.get("calificate", 0)