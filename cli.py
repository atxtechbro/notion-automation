import click
from notion_client.api import NotionClient
from notion_client.config import ConfigManager

@click.group()
def cli():
    pass

@cli.command()
@click.option('--schema', required=True, help='Schema name without extension.')
@click.option('--tasks', required=True, help='Tasks name without extension.')
def create_database(schema, tasks):
    # Implementation as above
    pass

if __name__ == "__main__":
    cli()
