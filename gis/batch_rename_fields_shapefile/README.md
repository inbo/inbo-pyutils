# GUI application to batch rename the fields of a shapefile

## Introduction

This code provides a user interface approach to batch rename the fieldnames (columnnames) of a shapefile. The code uses [tkinter](https://wiki.python.org/moin/TkInter) to provide the user interface and [pandas](https://pypi.python.org/pypi/pandas), [geopandas](https://pypi.python.org/pypi/geopandas) and [fiona](https://pypi.python.org/pypi/Fiona) to perform the conversion.



## Aim

The aim is to rename multiple fields in a shapefile table in one loop (unlike ArcMap, where fields have to be renamed one by one).



## Functionality

### Starting the GUI

The GUI application can be started from the command line as follows:

```python
python batch_rename_fields_shapefile.py
```

This will bring up the following GUI elements, in order:

* A window to select the input shapefile.

* A window to select the textfile which contains the old fieldnames and the new fieldnames.

  > The textfile is structured as follows:
  >
  > - header = None, delimiter = ";", lineterminator = "\n"
  > - old_fieldname_1;new_fieldname_1
  > - old_fieldname_2;new_fieldname_2
  > - ...

* A window to define the output location and the output filename.shp.

The renaming procedure will start automatically after the input are defined.