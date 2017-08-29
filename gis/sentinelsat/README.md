# Sentinel-2

## Introduction

This code provides a user interface approach to download, process and work with Sentinel-2 imagery.

The aim of this project is threefold:

1. to bulk download Sentinel-2 datasets from the Copernicus Open Access Hub,
2. to convert en process Sentinel-2 datasets to useful imagery (e.g. mosaics, RGB and NDVI images, ...),
3. to batch clip Sentinel-2 imagery with a certain study area.

Each of the aims is written as a standalone module, but "2" depends on the output of "1", while "3" uses the output of "2".

## Downloading Sentinel-2 datasets

### Introduction

This code provides a user interface approach to query and download Sentinel-2 datasets, covering Flanders (Belgium), from the [Copernicus Open Access Hub](https://scihub.copernicus.eu/). The code uses [tkinter](https://docs.python.org/3/library/tkinter.html) to provide the user interface, and the [sentinelsat](http://sentinelsat.readthedocs.io/en/master/index.html) utility to query and download Sentinel-2 satellite images. [collections](https://docs.python.org/3/library/collections.html) is used to access the results of the query, stored in a dictionary. *tkinter* and *collections* are part of [the Python Standard Library](https://docs.python.org/3/library/index.html).

### Functionality

...

### Example

To illustrate the functionality, an inline example is provided in a [notebook](https://github.com/inbo/inbo-pyutils/blob/sentinelsat/gis/sentinelsat/sentinel_data_download.ipynb).

## Processing Sentinel-2 datasets

### Introduction

This code provides a user interface approach to process downloaded Sentinel-2 datasets. 

The code uses:

- [tkinter](https://docs.python.org/3/library/tkinter.html): to provide the user interface, 

- [glob](https://docs.python.org/3/library/glob.html), [os](https://docs.python.org/3/library/os.html),  [shutil](https://docs.python.org/3/library/shutil.html) and [more_itertools](https://pypi.python.org/pypi/more-itertools): for various (data management) purposes,

- [zipfile](https://docs.python.org/3/library/zipfile.html): to unpack the downloaded zipped Sentinel-2 datasets, 

- [GDAL](https://pypi.python.org/pypi/GDAL), [rsgislib](http://www.rsgislib.org/), [rasterstats](https://pypi.python.org/pypi/rasterstats) and [numpy](http://www.numpy.org/): in the image processing chain.

  (*tkinter*, *glob*, *os*, *shutil* and *zipfile* are part of [the Python Standard Library](https://docs.python.org/3/library/index.html))

The code detects the imagery that overlaps with the bounding box of Flanders (Belgium), i.e. the following eight granules: 

- T31UDT - T31UET - T31UFT - T31UGT


- T31UDS - T31UES - T31UFS - T31UGS

Only the overlapping imagery is kept for further processing. Image processing results in four main outputs:

1. A **GeoTiff** for **each granule**

   Images (granules) are converted one by one from the JP2 to the GeoTiff fileformat. Coordinates are transformed from EPSG:32631 to EPSG:4326.

2. **Mosaic for each individual band**

   A mosaic of the available imagery per day for each of the 13 bands is created. Also one overview mosaic is produced. The output coordinate system is EPSG:4326, the fileformat is GeoTiff. The mosaic is cropped to the Flanders bounding box.

3. **RGB-image**

   An RGB (Red-Green-Blue) image is created by stacking band B02 (Blue), B03 (Green) and B04 (Red) into one GeoTiff. The code uses the mosaiced bands B02, B03 and B04 as input. The output coordinate system is EPSG:4326, the fileformat is GeoTiff.

4. **NDVI-image**

   Normalised Difference Vegetation Index. An NDVI image is created by performing a raster calculation using B04 (Red) and B08 (NIR): (B08 - B04) / (B08 + B04). The code uses the mosaiced bands B04 and B08 as input.The output coordinate system is EPSG:4326, the fileformat is GeoTiff.

### Functionality

...

### Example

To illustrate the functionality, an inline example is provided in a [notebook](https://github.com/inbo/inbo-pyutils/blob/sentinelsat/gis/sentinelsat/sentinel_processing.ipynb).



## Clip Sentinel-2 imagery with study area

### Introduction

This code provides a user interface approach to clip Sentinel-2 imagery with the bounding box of a chosen study area. The study area bounding box is provided as a [GeoJSON](http://geojson.org/) file. 

The code uses [tkinter](https://docs.python.org/3/library/tkinter.html) to provide the user interface, [GDAL](https://pypi.python.org/pypi/GDAL) to perform the clipping and [rasterstats](https://pypi.python.org/pypi/rasterstats) to conduct a 'No Data' check. [glob](https://docs.python.org/3/library/glob.html) and [os](https://docs.python.org/3/library/os.html) are used for various purposes. *tkinter*, *glob* and *os* are part of [the Python Standard Library](https://docs.python.org/3/library/index.html).

### Functionality

...

### Example

To illustrate the functionality, an inline example is provided in a [notebook](https://github.com/inbo/inbo-pyutils/blob/sentinelsat/gis/sentinelsat/sentinel_processing_clip_study_area.ipynb).