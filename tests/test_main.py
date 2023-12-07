"""Test cases for the __main__ module."""
import netCDF4
import pytest
from click.testing import CliRunner
from ncdump_rich import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def _make_ds() -> netCDF4.Dataset:
    ds = netCDF4.Dataset("test.nc", mode="w", format="NETCDF4")
    ds.description = "Example dataset"
    ds.creator = "Example dataset"
    _ = ds.createDimension("time", None)
    _ = ds.createVariable("time", "f8", ("time",))
    _ = ds.createDimension("lat", 10)
    _ = ds.createDimension("lon", 10)
    return ds


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    with runner.isolated_filesystem():
        # Many variables
        ds = _make_ds()
        for i in range(21):
            # fmt: off
            _ = ds.createVariable(f"{i}", "f4", ("time", "lat", "lon",),)[:] = [
                -90, -70, -50, -30, -10,
                10, 30, 50, 70, 90,
            ]  # south pole to north pole
            # fmt: on

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
        lat[:] = [
            i * 10 - 90 for i in range(nlats)
        ]  # -90.0 + (180.0 / nlats) * np.arange(nlats)  # south pole to north pole
        lon[:] = [
            180.0 / nlats * i for i in range(nlons)
        ]  # (180.0 / nlats) * np.arange(nlons)  # Greenwich meridian eastward
        data_arr = [[list(range(nlons)) for _ in range(nlats)] for _ in range(ntimes)]
        temp[:, :, :] = data_arr  # Appends data along unlimited dimension
        data_slice = [
            list(range(nlons)) for _ in range(nlats)
        ]  # np.random.uniform(low=280, high=330, size=(nlats, nlons))
        temp[3, :, :] = data_slice

        # Wrong file name
        with open("wrong.txt", "w") as f:
            f.write("Hello, World!")

        result = runner.invoke(__main__.main, ["test.nc"])
        result = runner.invoke(__main__.main, ["-s", "-F", "test.nc"])
        result = runner.invoke(__main__.main, ["-l", "-f", "test.nc"])
        result = runner.invoke(__main__.main, ["-l", "-F", "test.nc"])
        result = runner.invoke(__main__.main, ["test2.nc"])
        result = runner.invoke(__main__.main, ["-s", "-F", "test2.nc"])
        result = runner.invoke(__main__.main, ["-l", "-f", "test2.nc"])
        result = runner.invoke(__main__.main, ["-l", "-F", "test2.nc"])
        result = runner.invoke(__main__.main, ["wrong.txt"])
        ds.close()
        ncfile.close()
    assert result.exit_code == 0
