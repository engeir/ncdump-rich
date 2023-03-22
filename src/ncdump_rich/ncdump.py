"""Formatted output of a .nc file.

This script takes in as input with the `-i` `--input` flag a `.nc` file
and by default truncates the output if a lot of data exist,
so the most important information is presented.

The flag `-l` `--long` will override the truncation and print a long
output with all information contained in the .nc file.
"""
import pprint
import textwrap

import netCDF4  # type: ignore
from rich.console import Console


def ncdump(src_path: str, long: bool = False, truecolor: bool = True) -> None:
    """Output dimensions, variables and their attribute information.

    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Inspired by: http://schubert.atmos.colostate.edu/~cslocum/netcdf_example.html

    Parameters
    ----------
    src_path: str
        Path to a .nc file
    long: bool (default: False)
        Print all details found in the .nc file
    truecolor: bool (default: True)
        Print with colours and stylised font
    verb: bool (default: True)
        Whether or not nc_attrs, nc_dims, and nc_vars are printed
    """
    nc_file = netCDF4.Dataset(src_path, "r")
    if truecolor:
        console = Console(force_terminal=True, color_system="truecolor", tab_size=4)
    else:
        console = Console(tab_size=4)
    width = console.size.width
    cprint = console.print

    def print_ncattr(key: str) -> None:
        """Print the NetCDF file attributes for a given key.

        Parameters
        ----------
        key: str
            A valid netCDF4.Dataset.variables key
        """
        try:
            cprint(
                "\t\t[italic white]type:[/italic white]",
                repr(nc_file.variables[key].dtype),
            )
            for ncattr in nc_file.variables[key].ncattrs():
                cprint(
                    "\t\t[italic white]%s:[/italic white]" % ncattr,
                    repr(nc_file.variables[key].getncattr(ncattr)),
                )
        except KeyError:
            s1 = "\t\t[italic white]WARNING: [/italic white][red]"
            s2 = f"{key}[/red] does not contain variable attributes"
            cprint(s1 + s2)

    # Print file properties
    cprint("[bold white]NetCDF Properties:[/bold white]")
    for key, prop in {
        "File format": "file_format",
        "Disk format": "disk_format",
    }.items():
        cprint(f"\t[italic white]{key}[/italic white]: {getattr(nc_file, prop)}")

    # NetCDF global attributes
    nc_attrs = nc_file.ncattrs()
    cprint("[bold white]NetCDF Global Attributes:[/bold white]")
    for nc_attr in nc_attrs:
        if any(
            len(line) > width - 9
            for line in str(nc_file.getncattr(nc_attr)).splitlines()
        ):
            lineend = (
                " [italic white dim]4 spaces = new line; 8 spaces = line wrap[/italic"
                " white dim]\n\t\t"
            )
        else:
            lineend = " "
        try:
            if repr(nc_file.getncattr(nc_attr)[0]) != repr("\n"):
                cprint(
                    f"\t[italic white]{nc_attr}:[/italic white]{lineend}"
                    + "\n\t\t".join(
                        [
                            textwrap.fill(
                                " ".join(line.split()),
                                width=width - 9,
                                tabsize=4,
                                break_long_words=False,
                                replace_whitespace=False,
                                subsequent_indent="\t\t\t",
                            )
                            for line in str(nc_file.getncattr(nc_attr)).splitlines()
                        ]
                    ),
                )
            else:
                cprint(
                    f"\t[italic white]{nc_attr}:[/italic white]{lineend}"
                    + "\n\t\t".join(
                        [
                            textwrap.fill(
                                " ".join(line.split()),
                                width=width - 9,
                                tabsize=4,
                                break_long_words=False,
                                replace_whitespace=False,
                                subsequent_indent="\t\t\t",
                            )
                            for line in str(nc_file.getncattr(nc_attr)).splitlines()
                        ]
                    ),
                )
        except IndexError:
            cprint("\t[italic white]%s:[/italic white] [red]empty[/red]" % nc_attr)
    nc_dims = list(nc_file.dimensions)
    cprint("[bold white]NetCDF Dimension Information:[/bold white]")
    for dim in nc_dims:
        cprint("\t[italic white]Name:[/italic white]", dim)
        cprint("\t\t[italic white]size:[/italic white]", len(nc_file.dimensions[dim]))
        print_ncattr(dim)

    # Variable information.
    nc_vars = list(nc_file.variables)  # list of nc variables
    cprint("[bold white]NetCDF Variable Information:[/bold white]")
    if long:
        for var in nc_vars:
            if var not in nc_dims:
                cprint("\t[italic white]Name:[/italic white]", var)
                cprint(
                    "\t\t[italic white]dimensions:[/italic white]",
                    repr(nc_file.variables[var].dimensions),
                )
                cprint(
                    "\t\t[italic white]size:[/italic white]",
                    nc_file.variables[var].size,
                )
                print_ncattr(var)
    else:
        if len(nc_vars) > 20:
            cprint("\t[italic white]Number of variables: [/italic white]", len(nc_vars))
            cprint("\t[italic white]Variables list: [/italic white]")
            pp = pprint.PrettyPrinter(width=width - 9, compact=True)
            cprint(textwrap.indent(pp.pformat(nc_vars), "\t\t"))
        else:
            for var in nc_vars:
                if var not in nc_dims:
                    cprint("\t[italic white]Name:[/italic white]", var)
                    cprint(
                        "\t\t[italic white]dimensions:[/italic white]",
                        repr(nc_file.variables[var].dimensions),
                    )
                    cprint(
                        "\t\t[italic white]size:[/italic white]",
                        nc_file.variables[var].size,
                    )
                    print_ncattr(var)
