"""Command-line interface."""
import click
from hello_garden import server
from hello_garden import data

@click.command()
@click.version_option()
@click.option("--datafilename", help="Data filename")
@click.option("--database", help="Database filename")
@click.option("--debug/--no-debug", help="Debug mode", default=False)
def main(datafilename, database, debug) -> None:
    """Hello Garden."""
    data_items = data.get_data(datafilename)
    server.run(debug=debug, data=data_items, database=database)


if __name__ == "__main__":
    main(prog_name="hello-garden")  # pragma: no cover
