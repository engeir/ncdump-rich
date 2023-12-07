"""Formatted output of a .nc file.

This script takes in as input with the `-i` `--input` flag a `.nc` file
and by default truncates the output if a lot of data exist,
so the most important information is presented.

The flag `-l` `--long` will override the truncation and print a long
output with all information contained in the .nc file.
"""
import pprint
import textwrap

import netCDF4
from rich.console import Console

VAR_LIST_LIMIT = 20


class NcDump:
    """Output dimensions, variables and their attribute information.

    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Inspired by: http://schubert.atmos.colostate.edu/~cslocum/netcdf_example.html

    Parameters
    ----------
    src_path : str
        Path to a .nc file
    long : bool
        Print all details found in the .nc file. Default is False.
    truecolor : bool
        Print with colours and stylised font. Default is True.
    """

    def __init__(
        self, src_path: str, long: bool = False, truecolor: bool = True
    ) -> None:
        self.long = long
        self.nc_file = netCDF4.Dataset(src_path, "r")
        self.nc_vars = list(self.nc_file.variables)  # list of nc variables
        self.nc_dims = list(self.nc_file.dimensions)
        if truecolor:
            console = Console(force_terminal=True, color_system="truecolor", tab_size=4)
        else:
            console = Console(tab_size=4)
        self.width = console.size.width
        self.cprint = console.print

    def _print_ncattr(self, key: str) -> None:
        """Print the NetCDF file attributes for a given key.

        Parameters
        ----------
        key : str
            A valid netCDF4.Dataset.variables key
        """
        try:
            self.cprint(
                "\t\t[italic white]type:[/italic white]",
                repr(self.nc_file.variables[key].dtype),
            )
            for ncattr in self.nc_file.variables[key].ncattrs():
                self.cprint(
                    "\t\t[italic white]%s:[/italic white]" % ncattr,
                    repr(self.nc_file.variables[key].getncattr(ncattr)),
                )
        except KeyError:
            s1 = "\t\t[italic white]WARNING: [/italic white][red]"
            s2 = f"{key}[/red] does not contain variable attributes"
            self.cprint(s1 + s2)

    def print_file_props(self) -> None:
        """Print file properties."""
        self.cprint("[bold white]NetCDF Properties:[/bold white]")
        for key, prop in {
            "File format": "file_format",
            "Disk format": "disk_format",
        }.items():
            self.cprint(
                f"\t[italic white]{key}[/italic white]: {getattr(self.nc_file, prop)}"
            )

    def print_global_attrs(self) -> None:
        """Print the global attributes."""
        nc_attrs = self.nc_file.ncattrs()
        self.cprint("[bold white]NetCDF Global Attributes:[/bold white]")
        for nc_attr in nc_attrs:
            if any(
                len(line) > self.width - 9
                for line in str(self.nc_file.getncattr(nc_attr)).splitlines()
            ):
                lineend = (
                    " [italic white dim]4 spaces = new line; 8 spaces = line wrap[/italic"
                    " white dim]\n\t\t"
                )
            else:
                lineend = " "
            try:
                if repr(self.nc_file.getncattr(nc_attr)[0]) != repr("\n"):
                    self.cprint(
                        f"\t[italic white]{nc_attr}:[/italic white]{lineend}"
                        + "\n\t\t".join(
                            [
                                textwrap.fill(
                                    " ".join(line.split()),
                                    width=self.width - 9,
                                    tabsize=4,
                                    break_long_words=False,
                                    replace_whitespace=False,
                                    subsequent_indent="\t\t\t",
                                )
                                for line in str(
                                    self.nc_file.getncattr(nc_attr)
                                ).splitlines()
                            ]
                        ),
                    )
                else:
                    self.cprint(
                        f"\t[italic white]{nc_attr}:[/italic white]{lineend}"
                        + "\n\t\t".join(
                            [
                                textwrap.fill(
                                    " ".join(line.split()),
                                    width=self.width - 9,
                                    tabsize=4,
                                    break_long_words=False,
                                    replace_whitespace=False,
                                    subsequent_indent="\t\t\t",
                                )
                                for line in str(
                                    self.nc_file.getncattr(nc_attr)
                                ).splitlines()
                            ]
                        ),
                    )
            except IndexError:
                self.cprint(
                    "\t[italic white]%s:[/italic white] [red]empty[/red]" % nc_attr
                )
        self.cprint("[bold white]NetCDF Dimension Information:[/bold white]")
        for dim in self.nc_dims:
            self.cprint("\t[italic white]Name:[/italic white]", dim)
            self.cprint(
                "\t\t[italic white]size:[/italic white]",
                len(self.nc_file.dimensions[dim]),
            )
            self._print_ncattr(dim)

    def print_variable_props(self) -> None:
        """Print information about the variables."""
        self.cprint("[bold white]NetCDF Variable Information:[/bold white]")
        if not self.long and len(self.nc_vars) > VAR_LIST_LIMIT:
            self.cprint(
                "\t[italic white]Number of variables: [/italic white]",
                len(self.nc_vars),
            )
            self.cprint("\t[italic white]Variables list: [/italic white]")
            pp = pprint.PrettyPrinter(width=self.width - 9, compact=True)
            self.cprint(textwrap.indent(pp.pformat(self.nc_vars), "\t\t"))
        else:
            for var in self.nc_vars:
                if var not in self.nc_dims:
                    self.cprint("\t[italic white]Name:[/italic white]", var)
                    self.cprint(
                        "\t\t[italic white]dimensions:[/italic white]",
                        repr(self.nc_file.variables[var].dimensions),
                    )
                    self.cprint(
                        "\t\t[italic white]size:[/italic white]",
                        self.nc_file.variables[var].size,
                    )
                    self._print_ncattr(var)


def ncdump(src_path: str, long: bool = False, truecolor: bool = True) -> None:
    """Output dimensions, variables and their attribute information.

    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Inspired by: http://schubert.atmos.colostate.edu/~cslocum/netcdf_example.html

    Parameters
    ----------
    src_path : str
        Path to a .nc file
    long : bool
        Print all details found in the .nc file. Default is False.
    truecolor : bool
        Print with colours and stylised font. Default is True.
    """
    dump = NcDump(src_path, long, truecolor)
    dump.print_file_props()
    dump.print_global_attrs()
    dump.print_variable_props()
