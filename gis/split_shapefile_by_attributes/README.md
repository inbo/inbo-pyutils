
# GUI application to split a shapefile based on a field attribute

## Introduction

This code provides a user interface approach to split a shapefile on the attribute values of a given field. The code uses [fiona](https://pypi.python.org/pypi/Fiona) to perform the split and [tkinter](https://wiki.python.org/moin/TkInter) to provide a user interface. 

## Functionality

### Starting the GUI

Currently, the GUI-version can be started by starting the python script from the command line as follows:

```
python split_shapefile_by_attributes.py
```

The interface dialogs will appear to ask for the required inputs:
* The shapefile to use for the split
* The folder to save the resulting set of shapefiles
* A menu to select the field name on which the split is based

Click `Start splitting`... 


### Python function

The functionality itself is available as a python function `split_shape_by_attribute`, which can be imported as Python module.

When running the function inside Python, make sure the location is added to the PATH in order to enable the import of the function.

Similar to the GUI functionality, the python function `split_shape_by_attribute` reads an input file, request the information from GBIF and adds the required information from the mapping.

```
from split_shapefile_by_attributes import split_shape_by_attribute
split_shape_by_attribute("my_shapefile.shp", "./output_dir", "TAG")
```


