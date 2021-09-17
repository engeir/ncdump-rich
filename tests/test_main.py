"""Test cases for the __main__ module."""
import netCDF4  # type: ignore
import numpy as np
import pytest
from click.testing import CliRunner

from ncdump_rich import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    with runner.isolated_filesystem():
        # Many variables
        ds = netCDF4.Dataset("test.nc", mode="w", format="NETCDF4")
        ds.description = "Example dataset"
        ds.creator = "Example dataset"
        _ = ds.createDimension("time", None)
        _ = ds.createVariable("time", "f8", ("time",))
        _ = ds.createDimension("lat", 10)
        _ = ds.createDimension("lon", 10)
        for i in range(21):
            _ = ds.createVariable(f"{i}", "f4", ("time", "lat", "lon",),)[:] = -90.0 + (
                180.0 / 10
            ) * np.arange(
                10
            )  # south pole to north pole

        # Few variables
        ncfile = netCDF4.Dataset("test2.nc", mode="w", format="NETCDF4")
        # nc_attrs for loop
        ncfile.title = ""
        ncfile.description = "Example dataset"
        ncfile.creator = "\n"
        lat_dim = ncfile.createDimension("lat", 73)  # latitude axis
        lon_dim = ncfile.createDimension("lon", 144)  # longitude axis
        _ = ncfile.createDimension("novar")  # KeyError: No variable information
        _ = ncfile.createDimension("time", None)  # unlimited axis (can be appended to).
        lat = ncfile.createVariable("lat", float, ("lat",))
        lat.units = "degrees_north"
        lat.long_name = "latitude"
        lon = ncfile.createVariable("lon", float, ("lon",))
        lon.units = "degrees_east"
        lon.long_name = "longitude"
        time = ncfile.createVariable("time", float, ("time",))
        time.units = "hours since 1800-01-01"
        time.long_name = "time"
        temp = ncfile.createVariable(
            "temp", float, ("time", "lat", "lon")
        )  # note: unlimited dimension is leftmost
        temp.units = "K"  # degrees Kelvin
        temp.standard_name = "air_temperature"  # this is a CF standard name
        nlats = len(lat_dim)
        nlons = len(lon_dim)
        ntimes = 3
        lat[:] = -90.0 + (180.0 / nlats) * np.arange(nlats)  # south pole to north pole
        lon[:] = (180.0 / nlats) * np.arange(nlons)  # Greenwich meridian eastward
        data_arr = np.random.uniform(low=280, high=330, size=(ntimes, nlats, nlons))
        temp[:, :, :] = data_arr  # Appends data along unlimited dimension
        data_slice = np.random.uniform(low=280, high=330, size=(nlats, nlons))
        temp[3, :, :] = data_slice
        result = runner.invoke(__main__.main, ["-i", "test.nc"])
        result = runner.invoke(__main__.main, ["-s", "-F", "-i", "test.nc"])
        result = runner.invoke(__main__.main, ["-l", "-f", "-i", "test.nc"])
        result = runner.invoke(__main__.main, ["-l", "-F", "-i", "test.nc"])
        result = runner.invoke(__main__.main, ["-i", "test2.nc"])
        result = runner.invoke(__main__.main, ["-s", "-F", "-i", "test2.nc"])
        result = runner.invoke(__main__.main, ["-l", "-f", "-i", "test2.nc"])
        result = runner.invoke(__main__.main, ["-l", "-F", "-i", "test2.nc"])
        ds.close()
        ncfile.close()
    assert result.exit_code == 0
