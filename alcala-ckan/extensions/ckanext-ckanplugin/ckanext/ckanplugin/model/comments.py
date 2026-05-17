from sqlalchemy import Column, UnicodeText, Integer, ForeignKey,String,UniqueConstraint,DateTime
from ckan.model.meta import metadata
from ckan.model.types import make_uuid
from sqlalchemy.ext.declarative import declarative_base
import datetime as datetime
from zoneinfo import ZoneInfo

Base = declarative_base(metadata=metadata)

import json, logging,os,  mimetypes

log = logging.getLogger(__name__)

def get_local_time():
    return datetime.datetime.now(ZoneInfo("America/Bogota")) 

class Comments(Base):

    __tablename__ = 'Comments'

    id = Column(Integer, primary_key=True,autoincrement=True)
    package_Id = Column(String, nullable=False)
    comments = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    created = Column(DateTime, default=get_local_time)

    __table_args__ = (
        UniqueConstraint('package_Id',name='uix_source_package'),
    )

    def __init__(self,  package_Id=None,user_id=None,comments=None, **kwargs ):
        super().__init__(**kwargs)
        self.package_Id = package_Id
        self.user_id = user_id
        self.comments = comments


      
        