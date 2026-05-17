import click

@click.group()
def click_command_group():
    """Grupo de comandos para mi extensión."""
    pass

@click_command_group.command()
def ejecutar():
    """Ejecuta la acción de mi plugin."""
    click.echo("¡Comando ejecutado con éxito en CKAN moderno!")

