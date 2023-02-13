"""Command-line interface."""
import sys

import rich_click as click
from rich import print as rprint

import ncdump_rich.ncdump as ncd
from ncdump_rich import __version__

# click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
# click.rich_click.GROUP_ARGUMENTS_OPTIONS = True


@click.command()
@click.version_option(version=__version__)
@click.argument("filename", type=click.Path(exists=True, readable=True), required=True)
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
    help="Print in formatted text. No formatting is better when the output is stored "
    + "and viewed in an editor.",
)
def main(filename: str, long: bool, format: bool) -> None:
    """Rich NcDump.

    Read in a netCDF file as FILENAME and beautifully print a preview of it using
    [Rich](https://github.com/Textualize/rich).
    """
    if filename.endswith(".nc"):
        ncd.ncdump(filename, long=long, truecolor=format)
    else:
        rprint(
            "[bold]ncdump-rich[/bold] can only read [italic green].nc"
            + f"[/italic green] files, not [italic red].{filename.split('.')[-1]}"
            + "[/italic red]"
        )
        sys.exit()


if __name__ == "__main__":
    main(prog_name="ncdump-rich")  # pragma: no cover
