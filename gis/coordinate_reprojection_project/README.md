# COORDINATE REPROJECTION PROJECT

## WORK IN PROGRESS

This is work in progress (and full of errors). 

## AIM

The main AIM is to reproject projected coordinates (xyz) to a user-defined coordinate system (local xyz) (e.g. for data analysis and data visualisation). Before attacking the main challenges, we provide a series of 'basic' actions to deal with coordinates.

## OVERVIEW

1. ### Basic actions with coordinates

  This section comprises a series of 'basic' actions to deal with projected coordinates. The main idea is to be able to convert textfiles that contain xyz coordinates (e.g. GPS data collected during fieldwork) to shapefiles (or GeoJSON). One should be able to convert (a) the entire file, (b) a selection of the data based on attribute data, or (c) a selection of the data based on spatial location. Additionally, we want to switch between EPSG projections.
  An overview of the actions:

  * read coordinates from textfile (.txt) and convert these to a shapefile (or GeoJSON).
  * read coordinates from textfile (.txt), select coordinates by attribute and write these to shapefile (or GeoJSON).
  * read coordinates from textfile (.txt), select coordinates by spatial location and write these to shapefile (or GeoJSON).
  * switch from one EPSG projected coordinate system to another.
2. ### Main objectives/challenges

  The main AIM of this project is to reproject projected coordinates (xyz) to a user-defined coordinate system (local xyz). Therefore, three main objectives/challenges are pursued:

  * SHIFT from projected coordinates to user-defined coordinates.
  * SHIFT and ROTATE from projected coordinates to user-defined coordinates.
  * SHIFT, ROTATE and TILT from projected coordinates to user-defined coordinates (e.g. to visualise vertical data; soil profiles).
3. ### Ideas

  A series possible coordinate manipulations are currently on the ideas/thoughts level, but have potential to be useful.

  * SCALE (shrink/enlarge) to user-defined coordinate system (with/out rotation and/or tilt?)