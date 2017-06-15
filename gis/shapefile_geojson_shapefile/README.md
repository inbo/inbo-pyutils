# GUI application to batch convert shapefiles to GeoJSON

## Aim

The aim is to easily convert the ***ERSI shapefile*** filetype to the open source ***GeoJSON*** filetype.



## Introduction

This code provides a user interface approach to batch convert shapefiles to GeoJSON. [Tkinter](https://wiki.python.org/moin/TkInter) is used to provide the user interface. [Glob](https://docs.python.org/3/library/glob.html) is used enlist the shapefiles while [json](https://docs.python.org/3/library/json.html) and [pyshp](https://pypi.python.org/pypi/pyshp) are applied to perform the conversion.



## Functionality

Starting the GUI

The GUI application can be started from the command line as follows:

```python
python batch_convert_shapefile_to_geojson.py
```

This will bring up the following GUI elements, in order:

- A window to define the input directory storing the input shapefiles.
- A window to define the output directory where the output GeoJSON will be written.

The converting procedure will start automatically after the inputs are defined.



## Python function

The functionality itself is available as a python function batch_convert_shapefile_to_geojson, which can be imported as Python module.

When running the function inside Python, make sure the location is added to the PATH in order to enable the import of the function.

Similar to the GUI functionality, the python function batch_convert_shapefile_to_geojson requires an input directory and an output directory:

```python
from batch_convert_shapefile_to_geojson import batch_convert_shapefile_to_geojson
batch_conver_shapefile_to_geojson("my_input_directory", "my_output_directory")
```



## Example

To illustrate the functionality, an inline example is provided in the [notebook](https://github.com/inbo/inbo-pyutils/blob/shapefile_geojson_shapefile/gis/shapefile_geojson_shapefile/batch_convert_shapefile_to_geojson.ipynb).



## NOTE

This is work in progress.  Code to covert geojson to shapefile will be added soon.