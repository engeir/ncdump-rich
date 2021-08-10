"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner
from netCDF4 import Dataset

from ncdump_rich import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    with runner.isolated_filesystem():
        ds = Dataset("test.nc", mode="w", format="NETCDF4")
        _ = ds.description = "Example dataset"
        _ = ds.creator = "Example dataset"
        _ = ds.createDimension("time", None)
        _ = ds.createVariable("time", "f8", ("time",))
        _ = ds.createDimension("lat", 10)
        _ = ds.createDimension("lon", 10)
        for i in range(21):
            _ = ds.createVariable(
                f"{i}",
                "f4",
                (
                    "time",
                    "lat",
                    "lon",
                ),
            )
        ds2 = Dataset("test2.nc", mode="w", format="NETCDF4")
        _ = ds2.description = "Example dataset"
        _ = ds2.creator = "Example dataset"
        _ = ds2.createDimension("time", None)
        _ = ds2.createVariable("time", "f8", ("time",))
        _ = ds2.createDimension("lat", 10)
        _ = ds2.createDimension("lon", 10)
        _ = ds2.createVariable(
            "1",
            "f4",
            (
                "time",
                "lat",
                "lon",
            ),
        )
        result = runner.invoke(__main__.main, ["-i", "test.nc"])
        result = runner.invoke(__main__.main, ["-s", "-F", "-i", "test.nc"])
        result = runner.invoke(__main__.main, ["-l", "-f", "-i", "test.nc"])
        result = runner.invoke(__main__.main, ["-l", "-F", "-i", "test.nc"])
        result = runner.invoke(__main__.main, ["-i", "test2.nc"])
        result = runner.invoke(__main__.main, ["-s", "-F", "-i", "test2.nc"])
        result = runner.invoke(__main__.main, ["-l", "-f", "-i", "test2.nc"])
        result = runner.invoke(__main__.main, ["-l", "-F", "-i", "test2.nc"])
    assert result.exit_code == 0
