import matplotlib.pyplot as plt
import xarray as xr
import copernicusmarine
import numpy as np

day = "-01-01"
db_type = "_raw_vgo"

for year in range(1993, 2023):
    
    date = str(year) + day
    print(date)

    file = copernicusmarine.subset(
        output_directory="datasets",
        output_filename=date+db_type,
        username="", # à remplacer
        password="", # à remplacer
        dataset_id="dataset-armor-3d-rep-monthly",
        variables=["vgo"],
        minimum_longitude=-179.875,
        maximum_longitude=179.875,
        minimum_latitude=-82.125,
        maximum_latitude=89.875,
        start_datetime=date+"T00:00:00",
        end_datetime=date+"T00:00:00",
        minimum_depth=0,
        maximum_depth=5500,
    )

    data = xr.open_dataset(file.file_path)
    print(data.info)