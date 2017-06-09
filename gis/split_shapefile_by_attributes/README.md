# GUI application to split a shapefile based on a field attribute

## Introduction

This code provides a user interface approach to split a shapefile on the attribute values of a given field. The code uses [fiona](https://pypi.python.org/pypi/Fiona) to perform the split and [tkinter](https://wiki.python.org/moin/TkInter) to provide a user interface. 

## Functionality

### Starting the GUI

The GUI application can be started from the command line as follows:

```
python split_shapefile_by_attributes.py
```

This will bring up the following GUI elements, in order:

1. A window to select the shapefile you want to split
2. A window to select a directory to which the resulting shapefiles should be saved to
3. A menu to select the attribute name on which you want to split the shapefile

Click `Start splitting` to execute the split.

### Python function

The functionality itself is available as a python function `split_shape_by_attribute`, which can be imported as Python module.

When running the function inside Python, make sure the location is added to the PATH in order to enable the import of the function.

Similar to the GUI functionality, the python function `split_shape_by_attribute` requires an input file, an output directory and an attribute name:

```python
from split_shapefile_by_attributes import split_shape_by_attribute
split_shape_by_attribute("my_shapefile.shp", "./output_dir", "TAG")
```
