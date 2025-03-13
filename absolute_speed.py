import matplotlib.pyplot as plt
import xarray as xr
import copernicusmarine
import numpy as np

date = "2022-12-01"

file = copernicusmarine.subset(
    output_directory="datasets",
    output_filename="absolute_speed",
    username="", # à remplacer
    password="", # à remplacer
    skip_existing=True,
    dataset_id="dataset-armor-3d-rep-monthly",
    variables=["vgo", "ugo"],
    minimum_longitude=-179.875,
    maximum_longitude=179.875,
    minimum_latitude=-82.125,
    maximum_latitude=89.875,
    start_datetime=date+"T00:00:00",
    end_datetime=date+"T00:00:00",
    minimum_depth=0,
    maximum_depth=5500,
)

data = xr.open_dataset(file.file_path).sel(time=date, method="nearest").sel(depth=slice(0, 5000))

data = data.coarsen(latitude=4, longitude=4, boundary="pad").mean()
data["v"] = np.sqrt(np.square(data["ugo"]) + np.square(data["vgo"])).astype(np.float32)
data = data.drop_vars("ugo")
data = data.drop_vars("vgo")
data = data.reset_coords("time", drop=True)
print(data.info)
print(data["v"].min(), data["v"].max())

df = data.to_dataframe().dropna(subset=["v"])
df.to_csv("absolute_speed.csv")