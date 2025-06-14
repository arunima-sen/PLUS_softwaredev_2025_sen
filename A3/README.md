# Strava-like Hotspot Analysis (Salzburg)

This notebook simulates a [Strava](https://www.strava.com/) style activity analysis using synthetic GPS data for Salzburg, Austria. It applies spatial statistics to detect and visualize clusters of high activity durations.

## Overview

- Synthetic GPS data mimicking running/cycling patterns
- Coordinate transformation to UTM for spatial analysis
- Hotspot detection using Getis-Ord Gi* (PySAL)
- Visualization with Folium (interactive) and Matplotlib + Contextily (static)

## AI use disclaimer

The original Strava export was poorly formatted and too time-consuming to clean. Instead, I used ChatGPT to generate a synthetic dataset with realistic patterns for this analysis.

## Links

- [GeoPandas](https://geopandas.org/)
- [PySAL - Getis-Ord](https://pysal.org/esda/generated/esda.G_Local.html)
- [Folium - HeatMap](https://python-visualization.github.io/folium/latest/index.html)
