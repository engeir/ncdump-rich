"""Command-line interface."""
import click

import ncdump_rich.ncdump as ncd
from . import __version__


@click.command()
@click.version_option(version=__version__)
@click.option("--input", "-i", type=str, help="File name.")
@click.option(
    "--long/--short",
    "-l/-s",
    default=False,
    show_default=True,
    type=bool,
    help="Print all obtainable info from the .nc file.",
)
@click.option(
    "--format/--no-format",
    "-f/-F",
    default=True,
    show_default=True,
    type=bool,
    help="Print in formatted text. No formatting is better when the output is stored \
    and viewed in an editor.",
)
def main(input: str, long: bool, format: bool) -> None:
    """Rich NcDump."""
    ncd.ncdump(input, long=long, truecolor=format)


if __name__ == "__main__":
    main(prog_name="ncdump-rich")  # pragma: no cover
