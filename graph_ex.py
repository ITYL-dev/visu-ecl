import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import xarray as xr
import copernicusmarine
import numpy as np

file = copernicusmarine.subset(
    output_directory="datasets",
    output_filename="graph_ex",
    username="", # à remplacer
    password="", # à remplacer
    skip_existing=True,
    dataset_id="dataset-armor-3d-nrt-monthly",
    variables=["so", "to", "ugo", "vgo"],
    minimum_longitude=-179.875,
    maximum_longitude=179.875,
    minimum_latitude=-82.125,
    maximum_latitude=89.875,
    start_datetime="2024-12-01T00:00:00",
    end_datetime="2024-12-01T00:00:00",
    minimum_depth=0,
    maximum_depth=5500,
)

data = xr.open_dataset(file.file_path)

date = "2024-12-01"

print(data.info)

depth = data.coords["depth"].to_numpy()
latitude = data.coords["latitude"].to_numpy()
longitude = data.coords["longitude"].to_numpy()

win_lat = 30
win_long = 60

params = dict()

params["depth_value"] = depth.min()
params["start_lat"] = latitude[latitude.size//2] - win_lat//2 
params["start_long"] = longitude[longitude.size//2] - win_long//2
params["X"] = longitude[params["start_long"] <= longitude]
params["X"] = params["X"][params["X"] <= params["start_long"] + win_long]
params["Y"] = latitude[params["start_lat"] <= latitude]
params["Y"] = params["Y"][params["Y"] <= params["start_lat"] + win_lat]

subset = data.sel(time=date, method="nearest").sel(depth=params["depth_value"], method="nearest").sel(latitude=slice(params["start_lat"], params["start_lat"] + win_lat)).sel(longitude=slice(params["start_long"], params["start_long"] + win_long))
print(subset.info)

params["ugo"] = subset["ugo"].to_numpy()
params["vgo"] = subset["vgo"].to_numpy()
params["to"] = subset["to"].to_numpy()

def update():
    subset = data.sel(time=date, method="nearest").sel(depth=params["depth_value"], method="nearest").sel(latitude=slice(params["start_lat"], params["start_lat"] + win_lat)).sel(longitude=slice(params["start_long"], params["start_long"] + win_long))
    params["ugo"] = subset["ugo"].to_numpy()
    params["vgo"] = subset["vgo"].to_numpy()
    params["to"] = subset["to"].to_numpy()
    params["X"] = longitude[params["start_long"] <= longitude]
    params["X"] = params["X"][params["X"] <= params["start_long"] + win_long]
    params["Y"] = latitude[params["start_lat"] <= latitude]
    params["Y"] = params["Y"][params["Y"] <= params["start_lat"] + win_lat]
    quiver.set_UVC(params["ugo"], params["vgo"], [params["to"]])
    X, Y = np.meshgrid(params["X"], params["Y"])
    quiver.set_offsets(np.c_[X.ravel(), Y.ravel()])
    ax.set_xlim(X.min() - 1, X.max() + 1)
    ax.set_ylim(Y.min() - 1, Y.max() + 1)
    fig.canvas.draw_idle()

def update_depth(val):
    params["depth_value"] = val
    update()

def update_lat(val):
    params["start_lat"] = val
    update()

def update_long(val):
    params["start_long"] = val
    update()

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25, right=0.75)
quiver = ax.quiver(*np.meshgrid(params["X"], params["Y"]), params["ugo"], params["vgo"], [params["to"]])

ax_depth_slider = plt.axes([0.2, 0.1, 0.65, 0.03])  # Position of slider [left, bottom, width, height]
depth_slider = Slider(ax_depth_slider, 'Depth', depth.min(), depth.max(), valinit=depth.min(), valstep=depth)
depth_slider.on_changed(update_depth)

ax_lat_slider = plt.axes([0.8, 0.25, 0.03, 0.60])
lat_slider = Slider(ax_lat_slider, 'Lat', latitude.min(), latitude.max()-win_lat, orientation="vertical", valinit=params["start_lat"], valstep=latitude)
lat_slider.on_changed(update_lat)

ax_long_slider = plt.axes([0.9, 0.25, 0.03, 0.60])
long_slider = Slider(ax_long_slider, 'Long', longitude.min(), longitude.max()-win_long, orientation="vertical", valinit=params["start_long"], valstep=longitude)
long_slider.on_changed(update_long)

def on_click(event):
    if event.inaxes is None:
        return
    
    X, Y = np.meshgrid(params["X"], params["Y"])
    
    distances = np.sqrt((X - event.xdata) ** 2 + (Y - event.ydata) ** 2)
    
    index = np.unravel_index(np.argmin(distances), distances.shape)
    
    print(f"Selected arrow index: {index}")
    print(f"Arrow position: ({X[index]}, {Y[index]})")
    print(f"Ugo selected arrow: {params['ugo'][index]}")
    print(f"Vgo selected arrow: {params['vgo'][index]}")
    print(f"To selected arrow: {params['to'][index]}")

    params["selected_point"] = (X[index], Y[index])

fig.canvas.mpl_connect("button_press_event", on_click)

plt.show()

long, lat = params["selected_point"]
print(lat, long)
subset = data.sel(time=date, method="nearest").sel(latitude=lat, method="nearest").sel(longitude=long, method="nearest")

ugo = subset["ugo"].to_numpy()
vgo = subset["vgo"].to_numpy()
to = subset["to"].to_numpy()
so = subset["so"].to_numpy()
v = np.sqrt(ugo**2 + vgo**2)

plt.figure()
plt.subplot(5,1,1)
plt.plot(depth, to, "-o")
plt.ylabel("Temperature [°C]")
plt.subplot(5,1,2)
plt.plot(depth, so, "-o")
plt.ylabel("Salinity [0.001]")
plt.subplot(5,1,3)
plt.plot(depth, ugo, "-o")
plt.ylabel("Eastward velocity [m/s]")
plt.subplot(5,1,4)
plt.plot(depth, vgo, "-o")
plt.ylabel("Northward velocity [m/s]")
plt.subplot(5,1,5)
plt.plot(depth, v, "-o")
plt.ylabel("Absolute velocity [m/s]")
plt.xlabel("Depth [m]")
plt.show()