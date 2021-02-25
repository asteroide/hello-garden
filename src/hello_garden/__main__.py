"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Hello Garden."""


if __name__ == "__main__":
    main(prog_name="hello-garden")  # pragma: no cover
