import netCDF4

ds = netCDF4.Dataset("test.nc", mode="w", format="NETCDF4")
ds.description = "Example description"
ds.creator = (
    "Example creator. Here, we make the line so long that it has to wrap. Notice that"
    " the line in this case will start on the next line, as opposed to the"
    " 'description' variable above. Newlines inside the description is indented with"
    " four spaces, while lines that have been wrapped are indented with eight spaces."
    " This is also printed with a dim colour where the variable name is. Can you see"
    " it?\n It is not so easy to see, but that is also the point, since it does not"
    " really provide any useful information; you only need to know about it and then it"
    " should be unobtrusive othervise. At this point I dont have anything more to say,"
    " I am just making sure the line is long enough to get some wrapping."
)
_ = ds.createDimension("time", None)
_ = ds.createVariable("time", "f8", ("time",))
_ = ds.createDimension("lat", 10)
_ = ds.createDimension("lon", 10)
for i in range(21):
    # fmt: off
    _ = ds.createVariable(f"very_long_variable_name_so_it_has_to_wrap_{i}", "f4", ("time", "lat", "lon",),)[:] = [
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
