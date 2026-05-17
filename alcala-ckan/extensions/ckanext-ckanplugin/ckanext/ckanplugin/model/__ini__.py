# models/__init__.py
from ckan.model.meta import metadata, DeclarativeBase

# Importas la clase de cada modelo desde su respectivo archivo
from .comments import Comments
from .contador import Contador
from .package_ext import Extend_package_table
from .resourceRating import ResourceRating

