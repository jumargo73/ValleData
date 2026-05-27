import click
from alembic.config import Config
from alembic import command
import os
from flask import current_app
from ckan.cli import load_config 

# 1. Definimos el grupo de comandos en minúsculas (igual que hace harvest)
@click.group(name='ckanplugin')
def click_command_group():
    """Grupo de comandos para la extensión ckanplugin."""
    pass

# 2. Registramos el subcomando específico para tus migraciones
@click_command_group.command(name='dbinit')
@click.pass_context
def initdb_command(ctx):
    """Inicializa y migra las tablas de base de datos de la extensión."""
    try:
        
        try:
            current_app = ctx.obj.app
        except AttributeError:
            click.echo("ERROR CRÍTICO: No se pudo obtener la instancia de la aplicación desde el contexto de CKAN.")
            return
        
        with current_app.app_context():
            
            # RUTA DINÁMICA ABSOLUTA: 
            # os.path.dirname(__file__) obtiene la ubicación exacta de este archivo 'plugin_logic.py'
            # Luego concatenamos la subcarpeta 'migration' de tu extensión
            base_dir = os.path.dirname(__file__)
            alembic_cfg_path = os.path.abspath(
                os.path.join(base_dir, 'migration', 'ckanplugin', 'alembic.ini')
            )
            
            click.echo(f"Buscando archivo de configuración en: {alembic_cfg_path}")
            
            if not os.path.exists(alembic_cfg_path):
                click.echo(f"ERROR: No se encontró el archivo físico en {alembic_cfg_path}")
                return
            
            # Unimos la ruta para encontrar el archivo alembic.ini de la extensión
            alembic_ini_file = os.path.join(migration_path, "alembic.ini")

            click.echo(f"Buscando archivo de configuración en: {alembic_ini_file}")
            if not os.path.exists(alembic_ini_file):
                raise FileNotFoundError(f"No se encontró el archivo alembic.ini en la ruta calculada: {alembic_ini_file}")

            # Extraer la URL de conexión a PostgreSQL de la configuración actual de CKAN
            sqlalchemy_url = current_app.config.get('sqlalchemy.url')
            if not sqlalchemy_url:
                raise ValueError("No se pudo obtener la cadena 'sqlalchemy.url' desde la configuración de CKAN.")

            # Inicializar y configurar Alembic en caliente
            cfg = Config(alembic_ini_file)
            cfg.set_main_option("sqlalchemy.url", sqlalchemy_url)

            # Forzar la ejecución de las migraciones
            click.echo("Aplicando scripts de migración Alembic (upgrade head)...")
            command.upgrade(cfg, "head")
            
            click.echo("Base de datos de la extensión inicializada y migrada con éxito.")

    except Exception as e:
        click.echo(f"ERROR CRÍTICO durante la migración: {str(e)}", err=True)
        raise click.Abort() 
    
    