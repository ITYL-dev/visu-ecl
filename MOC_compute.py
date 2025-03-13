import xarray as xr
import numpy as np

R = 6371e3  # Earth radius [m]

day = "-01-01"

mocs = []

for year in range(1993, 2023):
    date = str(year) + day
    print(date)

    data = xr.open_dataset("datasets/" + date + "_raw_vgo.nc")
    lat = data["latitude"]
    depth = data["depth"]
    lon = data["longitude"]
    v = data["vgo"]
    
    dx = (2 * np.pi * R * np.cos(np.deg2rad(lat))) / len(lon)  # Width of grid cells [m]

    # Compute meridional transport [m²/s] by integrating speed over longitude
    transport = []
    for i,l in enumerate(lat):
        transport.append((v.sel(latitude=l)*dx[i]).sum(dim="longitude"))
    transport = xr.concat(transport, dim="latitude")

    # Compute overturning [m³/s] streamfunction by integrating from the bottom up
    moc = []
    for i in range(len(depth)-1):
        dz = depth[i+1]-depth[i]
        moc.append(transport.sel(depth=depth[i])*dz)
    moc = xr.concat(moc, dim="depth")
    moc = moc.isel(depth=slice(None,None,-1)).cumsum(dim="depth").isel(depth=slice(None,None,-1))

    moc /= 1e6 # Convert to Sverdrups (Sv) (1 Sv = 10^6 m³/s)

    mocs.append(moc)

mocs = xr.concat(mocs, dim="time")
print(mocs)
df = mocs.to_dataset(name="moc").to_dataframe()
df.to_csv("MOC.csv")