"""

This .py file contains reusable geospatial functions for analyzing GPS-based activity data,
such as Strava-style points collected from walking, running, or cycling!

The dataset is expected to contain the columns: location, activity_type (e.g., walk, ride), duration_min, lat, lon

Functions include:
- Loading + cleaning the data as a geo dataframe
- Tagging activities based on duration
- Filtering by activity type
- Creating buffer zones
- Generating activity density using KDE
- Creating a fishnet grid and counting points
- Summarizing activity duration statistics by type

All spatial operations assume data is located in Salzburg, Austria (EPSG:32633 for UTM projection)


"""

import pandas as pd
import geopandas as gpd
import numpy as np
import shapely.geometry
from shapely.geometry import Point
from sklearn.neighbors import KernelDensity


def load_geodata(csv_path):
    """
    load csv w lat/lon and duration_min, return geodf

    """
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["lat", "lon", "duration_min"])
    df["duration_min"] = pd.to_numeric(df["duration_min"], errors="coerce")

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["lon"], df["lat"]),
        crs="EPSG:4326"
    )
    return gdf


def tag_zones_by_duration(gdf):
    """
    add duration_type column -  'short', 'medium', 'long' based on duration_min

    """
    bins = [0, 20, 40, np.inf]
    labels = ["short", "medium", "long"]
    gdf["duration_type"] = pd.cut(gdf["duration_min"], bins=bins, labels=labels)
    return gdf


def filter_by_activity(gdf, activity):
    """
    filter geodf by activity_type

    """
    return gdf[gdf["activity_type"].str.lower() == activity.lower()]


def calculate_density(gdf, bandwidth=100):
    """
    apply KDE to points

    """
    coords = np.vstack([gdf.geometry.x, gdf.geometry.y]).T
    kde = KernelDensity(bandwidth=bandwidth)
    kde.fit(coords)
    return np.exp(kde.score_samples(coords))


def create_buffers(gdf, buffer_radius_m=100):
    """
    create buffers of given radius (m) around points - returns buffered geodf

    """
    gdf_utm = gdf.to_crs("EPSG:32633")
    gdf_utm["buffer"] = gdf_utm.geometry.buffer(buffer_radius_m)
    return gdf_utm.set_geometry("buffer")


def generate_activity_grid(gdf, cell_size=250):
    """
    create fishnet grid 

    """
    bounds = gdf.total_bounds
    xmin, ymin, xmax, ymax = bounds

    cols = np.arange(xmin, xmax + cell_size, cell_size)
    rows = np.arange(ymin, ymax + cell_size, cell_size)

    polygons = [
        shapely.geometry.box(x, y, x + cell_size, y + cell_size)
        for x in cols[:-1] for y in rows[:-1]
    ]

    grid = gpd.GeoDataFrame(geometry=polygons, crs=gdf.crs)

    joined = gpd.sjoin(gdf, grid, how="left", predicate="within")
    counts = joined.groupby("index_right").size()
    grid["activity_count"] = counts
    grid["activity_count"] = grid["activity_count"].fillna(0)

    return grid


def compute_activity_stats_by_type(gdf):
    """
    summary statistics for duration_min grouped by activity_type
    """
    return gdf.groupby("activity_type")["duration_min"].describe()
