# Rich NcDump

[![PyPI](https://img.shields.io/pypi/v/ncdump-rich.svg)](https://pypi.org/project/ncdump-rich/)
[![Status](https://img.shields.io/pypi/status/ncdump-rich.svg)](https://pypi.org/project/ncdump-rich/)
[![Python Version](https://img.shields.io/pypi/pyversions/ncdump-rich)](https://pypi.org/project/ncdump-rich)
[![License](https://img.shields.io/pypi/l/ncdump-rich)](https://opensource.org/licenses/GPL-3.0)
[![Read the Docs](https://img.shields.io/readthedocs/ncdump-rich/latest.svg?label=Read%20the%20Docs)](https://ncdump-rich.readthedocs.io/)
[![Tests](https://github.com/engeir/ncdump-rich/workflows/Tests/badge.svg)](https://github.com/engeir/ncdump-rich/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/engeir/ncdump-rich/branch/main/graph/badge.svg)](https://codecov.io/gh/engeir/ncdump-rich)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- TODO

## Requirements

- TODO

## Installation

You can install _Rich NcDump_ via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):

```sh
pip install ncdump-rich
```

or perhaps even better via [pipx](https://github.com/pypa/pipx):

```sh
pipx install ncdump-rich
```

## Usage

Please see the [Command-line Reference](https://ncdump-rich.readthedocs.io/en/latest/usage.html) for details.

### Examples

Use the program as a previewer for `.nc` files, for example through [stpv](https://github.com/Naheel-Azawy/stpv).
My own fork, [stpv](https://github.com/engeir/stpv), provides additional support for
previewing `.nc` files using this project.

Similarly you can get preview of `.nc` files in [nnn](https://github.com/jarun/nnn) by
including an option for the extension `nc` in the [`preview-tui` plugin](https://github.com/jarun/nnn/blob/fc00faf7d0f4cd0b4637e719af52100861e8c17a/plugins/preview-tui#L247).

```sh
nc) fifo_pager ncdump-rich -i "$1" ;;
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide](CONTRIBUTING.rst).

## License

Distributed under the terms of the [GPL 3.0 license](https://opensource.org/licenses/GPL-3.0),
_Rich NcDump_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue](https://github.com/engeir/ncdump-rich/issues) along with a detailed description.

## Credits

This project was generated from [@cjolowicz](https://github.com/cjolowicz)'s [Hypermodern Python Cookiecutter](https://github.com/cjolowicz/cookiecutter-hypermodern-python) template.
