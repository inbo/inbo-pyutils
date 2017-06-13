import os
import sys

# import tkinter
from tkinter import Tk
import tkinter.filedialog as tkfd
import tkinter.simpledialog as tksd

import fiona
import pandas as pd
import geopandas as gpd


def gui_inputs():
    """Creates a GUI interface and returns the required inputs. 

    Returns
    -------
    input_shapefile : str
        path name to the shapefile with the 'to be converted' fieldnames/columnnames 

    info_file : str
        pathname to the textfile with the old and new fieldnames. The file is structured as follows: 
        header = None, delimiter = ";", lineterminator = "\n", e.g. 
            old_fieldname_1;new_fieldname_1
            old_fieldname_2;new_fieldname_2
            ...

    output_shapefile : str
        path name to the output shapefile

    """

    root = Tk()
    print("Select input shapefile")
    input_shapefile = tkfd.askopenfilename(title = "Select input shapefile", 
                                       initialdir = "C:/", 
                                       filetypes = (("shapefile", "*.shp"),("all files", "*.*")))

    print("Select input textfile")
    info_file = tkfd.askopenfilename(title = "Select textfile", 
                                 initialdir = "C:/", 
                                 filetypes = (("textfile", "*.txt"),("all files", "*.*")))

    print("Select output location and define output filename.shp - don't forget to add the .shp extension")
    output_shapefile = tkfd.asksaveasfilename(title = "Select output location and define output filename.shp", 
                                          initialdir = "C:/", 
                                          filetypes = (("shapefile", ".shp"), ("all types", "*.*")))
    root.destroy()

    return input_shapefile, info_file, output_shapefile


def batch_rename_field_shapefile(input_shapefile, info_file, output_shapefile):
    '''Batch rename the fields of a shapefile

    Using a for loop, the old fieldnames are replaced by the new fieldnames

    Parameters
    -----------
    input_shapefile : str
        path name to the shapefile with the 'to be converted' fieldnames/columnnames 
    info_file : str
        pathname to the textfile with the old and new fieldnames. The file is structured as follows: 
        header = None, delimiter = ";", lineterminator = "\n", e.g. 
            old_fieldname_1;new_fieldname_1
            old_fieldname_2;new_fieldname_2
            ...
    output_shapefile : str
        path name to the output shapefile

    '''
    # read the input shapefile
    shapefile = gpd.read_file(input_shapefile)
    # read the input textfile
    mapping = pd.read_csv(info_file, delimiter = ";", lineterminator = "\n", header = None)
    # Columnnames 'from' (old fieldnames) and 'to' (new fieldnames) are assigned to the columns in the textfile.
    mapping.columns = ('from', 'to')
    # Creates a dictionary which includes with the old fieldnames as index and the new fieldnames as keys.
    dict_mapping = mapping.set_index('from').to_dict()['to']
    # For loop to replace the old fieldnames by the new fieldnames.
    new_names = []
    for name in shapefile.columns:
        if name in dict_mapping.keys():
            new_names.append(dict_mapping[name])
        else:
            new_names.append(name)
    # Assign the new fieldnames as column headers (fieldnames) in the shapefile.
    shapefile.columns = new_names
    # Write the shapefile with the new fieldnames to the defined location.
    shapefile.to_file(output_shapefile)


def main(argv=None):
    """
    """
    print("starting GUI...")
    input_shapefile, info_file, output_shapefile = gui_inputs()
    
    print("Start renaming fields...")
    batch_rename_field_shapefile(input_shapefile, info_file, output_shapefile)
    print("... renaming completed!")


if __name__ == "__main__":
    sys.exit(main())
