
import os
import sys

import tkinter.filedialog as tkfd
import tkinter.simpledialog as tksd

import fiona

def gui_inputs():
    """
    """
    # locate your input shapefile
    infile = tkfd.askopenfilename(title = "Select your shapefile", 
                                initialdir = "C:/", 
                                filetypes = (("shapefile", "*.shp"), 
                                             ("all files", "*.*")))

    # define destination -folder- where output -shapefiles- will be written
    dest = tkfd.askdirectory(title = "Select your output folder", 
                            initialdir = "C:/")

    # define field to split by attributes
    field = tksd.askstring("Field", "Enter the name of the field to conduct the split by attributes on")

    return infile, field, dest


def split_shape_by_attribute(infile, field, dest):
    """split by attributes for shapefiles

    Works fine, for both unique and non-unique attribute values! Records with the 
    same attributes are grouped in seperate, new shapefiles...

    Parameters
    ----------
    infile : str
        filename of the input shapefile
    field : str
        name of the atrribute table field
    dest : str
        define destination -folder- where output -shapefiles- 
        will be written
    """
    with fiona.open(infile) as source:
        meta = source.meta
        for f in source:
            outfile = os.path.join(dest, "%s.shp" % f['properties'][field])
            try:
                with fiona.open(outfile, 'a', **meta) as sink:
                    sink.write(f)
            except:
                with fiona.open(outfile, 'w', **meta) as sink:
                    sink.write(f)

def main(argv=None):
    """
    """     

    infile, field, dest = gui_inputs()
    
    print("Start splitting procedure...")
    split_shape_by_attribute(infile, field, dest)
    print("... slitting completed!")


if __name__ == "__main__":
    sys.exit(main())