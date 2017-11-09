import os
import sys
from glob import glob

# import gui tkinter
from tkinter import Tk
import tkinter.filedialog as tkfd

import shapefile
from json import dumps

def gui_inputs():
    """Creates a GUI interface and returns the required inputs. 

    Returns
    -------
    input_directory : str
        path name to directory storing the input shapefiles. 

    output_directory : str
        path name to the directory where the output geojson will be written.

    """
    root = Tk()
    print("Select input folder")
    input_directory = tkfd.askdirectory(title = "Select input folder", initialdir = "C:/")

    print("Select output folder")
    output_directory = tkfd.askdirectory(title = "Select output folder", initialdir = "C:/")
    root.destroy()

    return input_directory, output_directory

def batch_convert_shapefile_to_geojson(input_directory, output_directory):
    '''Batch convert shapefiles to geojson

    Parameters
    -----------
    input_directory : str
        path name to directory storing the input shapefiles. 
    output_directory : str
        path name to the directory where the output geojson will be written.

    '''

    for path in glob(os.path.join(input_directory,"**", "*.shp"),recursive=True):
        # define the filename
        basename = os.path.basename(path)
        filename, file_extention = os.path.splitext(basename)

        # read the shapefile
        reader = shapefile.Reader(path)
        fields = reader.fields[1:]
        field_names = [field[0] for field in fields]
        buffer = []
        for sr in reader.shapeRecords():
            atr = dict(zip(field_names, sr.record))
            geom = sr.shape.__geo_interface__
            buffer.append(dict(type="Feature", geometry=geom, properties=atr)) 
   
        # write the GeoJSON file
        geojson = open(output_directory + "/" + filename + ".json", "w")
        geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
        geojson.close()


def main(argv=None):
    """
    """
    print("starting GUI...")
    input_directory, output_directory = gui_inputs()
    
    print("Start conversion from shapefile to geojson...")
    batch_convert_shapefile_to_geojson(input_directory, output_directory)
    print("... conversion completed!")


if __name__ == "__main__":
    sys.exit(main())
