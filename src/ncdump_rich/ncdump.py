"""Formatted output of a .nc file.

This script takes in as input with the `-i` `--input` flag a `.nc` file
and by default truncates the output if a lot of data exist,
so the most important information is presented.

The flag `-l` `--long` will override the truncation and print a long
output with all information contained in the .nc file.
"""
import pprint
import textwrap

from netCDF4 import Dataset
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
    nc_file = Dataset(src_path, "r")
    if truecolor:
        console = Console(force_terminal=True, color_system="truecolor", width=200)
    else:
        console = Console(width=200)
    print = console.print

    def print_ncattr(key: str) -> None:
        """Prints the NetCDF file attributes for a given key.

        Parameters
        ----------
        key: str
            A valid netCDF4.Dataset.variables key
        """
        try:
            print(
                "\t\t[italic white]type:[/italic white]",
                repr(nc_file.variables[key].dtype),
            )
            for ncattr in nc_file.variables[key].ncattrs():
                print(
                    "\t\t[italic white]%s:[/italic white]" % ncattr,
                    repr(nc_file.variables[key].getncattr(ncattr)),
                )
        except KeyError:
            s1 = "\t\t[italic white]WARNING: [/italic white][red]"
            s2 = "%s[/red] does not contain variable attributes" % key
            print(s1 + s2)

    # NetCDF global attributes
    nc_attrs = nc_file.ncattrs()
    print("[bold white]NetCDF Global Attributes:[/bold white]")
    for nc_attr in nc_attrs:
        if repr(nc_file.getncattr(nc_attr)[0]) != repr("\n"):
            print(
                "\t[italic white]%s:[/italic white]" % nc_attr,
                textwrap.fill(
                    str(nc_file.getncattr(nc_attr)),
                    subsequent_indent="\t\t",
                    break_long_words=False,
                    break_on_hyphens=False,
                ),
            )
        else:
            print(
                "\t[italic white]%s:[/italic white]" % nc_attr,
                textwrap.indent(str(nc_file.getncattr(nc_attr)), "\t\t"),
            )
    nc_dims = [dim for dim in nc_file.dimensions]  # list of nc dimensions

    # Dimension shape information.
    print("[bold white]NetCDF dimension information:[/bold white]")
    for dim in nc_dims:
        print("\t[italic white]Name:[/italic white]", dim)
        print("\t\t[italic white]size:[/italic white]", len(nc_file.dimensions[dim]))
        print_ncattr(dim)

    # Variable information.
    nc_vars = [var for var in nc_file.variables]  # list of nc variables
    print("[bold white]NetCDF variable information:[/bold white]")
    if long:
        for var in nc_vars:
            if var not in nc_dims:
                print("\t[italic white]Name:[/italic white]", var)
                print(
                    "\t\t[italic white]dimensions:[/italic white]",
                    repr(nc_file.variables[var].dimensions),
                )
                print(
                    "\t\t[italic white]size:[/italic white]",
                    nc_file.variables[var].size,
                )
                print_ncattr(var)
    else:
        if len(nc_vars) > 20:
            print("\t[italic white]Number of variables: [/italic white]", len(nc_vars))
            print("\t[italic white]Variables list: [/italic white]")  # , '\n', nc_vars)
            pp = pprint.PrettyPrinter(width=80, compact=True)
            print(textwrap.indent(pp.pformat(nc_vars), "\t\t"))
            # pprint.pprint(nc_vars)
        else:
            for var in nc_vars:
                if var not in nc_dims:
                    print("\t[italic white]Name:[/italic white]", var)
                    print(
                        "\t\t[italic white]dimensions:[/italic white]",
                        repr(nc_file.variables[var].dimensions),
                    )
                    print(
                        "\t\t[italic white]size:[/italic white]",
                        nc_file.variables[var].size,
                    )
                    print_ncattr(var)
