"""crear_tablas

Revision ID: 61b512870a7e
Revises: 
Create Date: 2026-05-17 15:49:43.416870

"""
from alembic import op
import sqlalchemy as sa
import datetime as datetime


# revision identifiers, used by Alembic.
revision = '61b512870a7e'
down_revision = None
branch_labels = ('CkanPlugin',)
depends_on = None


def upgrade():
   # 1. TABLA: ResourceRating
    op.create_table(
        'resource_rating',  # El nombre real que tendrá en PostgreSQL
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('package_Id', sa.UnicodeText(), nullable=False),
        sa.Column('ratings', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['package_Id'], ['package.id'], ondelete='CASCADE')
    )

    # 2. TABLA: Comments
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('package_Id', sa.UnicodeText(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('user_id', sa.String(length=100), nullable=True),        
        sa.Column('created', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['package_Id'], ['package.id'], ondelete='CASCADE')
    )

    # 3. TABLA: Contador
    op.create_table(
        'contador',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('package_Id',sa.UnicodeText(), nullable=False),
        sa.Column('source_Id',sa.String, nullable=False),
        sa.Column('contVistas',sa.Integer, nullable=False,default=0),
        sa.Column('contDownload',sa.Integer, nullable=False,default=0),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['package_Id'], ['package.id'], ondelete='CASCADE')
    )

    # 4. EXTENSIÓN DE LA TABLA PACKAGE CORE
    # Inyectamos físicamente las 4 columnas en la tabla package nativa de CKAN
    op.add_column('package', sa.Column('category', sa.UnicodeText(), nullable=True))
    op.add_column('package', sa.Column('city', sa.UnicodeText(), nullable=True))
    op.add_column('package', sa.Column('department', sa.UnicodeText(), nullable=True))
    op.add_column('package', sa.Column('update_frequency', sa.UnicodeText(), nullable=True))


def downgrade():
    # Pasos para revertir en orden inverso (por seguridad)
    op.drop_column('package', 'category')
    op.drop_column('package', 'update_frequency')
    op.drop_column('package', 'department')
    op.drop_column('package', 'city')
    op.drop_table('contador')
    op.drop_table('comments')
    op.drop_table('resource_rating')


