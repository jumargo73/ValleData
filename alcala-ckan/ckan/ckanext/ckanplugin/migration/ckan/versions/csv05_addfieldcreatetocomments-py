"""add_created_to_comments

Revision ID: <generado_automaticamente>
Revises: <id_anterior>
"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = 'csv05'
down_revision = 'csv04'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Agregar la columna permitiendo nulos temporalmente para no romper datos viejos
    op.add_column('Comments', 
        sa.Column('created', sa.DateTime(), nullable=True)
    )
    
    # 2. (Opcional) Llenar los registros viejos con la fecha actual para que no queden vacíos
    current_time = datetime.datetime.utcnow()
    op.execute(
        f"UPDATE Comments SET created = '{current_time.strftime('%Y-%m-%d %H:%M:%S')}' WHERE created IS NULL"
    )
    
    # 3. Alterar la columna para que sea obligatoria de ahora en adelante (opcional)
    # op.alter_column('ext_dataset_comment', 'created', nullable=False)

def downgrade():
    # Eliminar la columna en caso de hacer un rollback
    op.drop_column('Comments', 'created')
