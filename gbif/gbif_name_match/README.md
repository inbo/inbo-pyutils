# Match a set of species names with the GBIF taxonomic backbone

## Introduction

Working with different partners/institutes/researchers results in a diversity of taxonomic names to define species. This hardens comparison amongst datasets, as in many occasions, aggrgeation is aimed for or filtering on specific species. By translating all species names to a common taxonomic backbone (ensuring unique ID's for each species name), this can be done. 

## Aim

This small utility provides the functionality to add the species information from the GBIF backbone to any data table (CSV-style or a Pandas dataframe) by requesting this information via the GBIF API. For each match, the corresponding accepted name is looked for. Nevertheless there will always be errors and control is still essential, the acceptedkeys provide the ability to compare species names from different data sources.

## Functionality

The functionality can be loaded within Python itself by importing the function `extract_species_information` or by running the script from the command line.

### Command line function

To check the functionality of the command line function, request for help as follows:

```python
python gbif_species_name_match.py --help
```

The different arguments are as follows:

**Positional arguments:**

* `input_file`: the relative path and filename containing the species to request the info
* `output_file`: output file name (can be same as the input file)

**Optional arguments**:

* `--update`: the columns are updated instead of added (False when not selected)
* `--namecol`: column header from which to read the scientific name; if None, an automatic derivation is attempted (default: None)
* `--kingdomcol`: column header from which to read the kingdom; if None, an automatic derivation is attempted (default: None)
* `--strict`: Perform the GBIF API strict (False when not selected)
* `--api_terms`: specify the names to extract from the GBIF API request, default: usageKey scientificName canonicalName status rank matchType confidence. If  `all`, the entire message is taken into columns

As an example, the following code will execute the matching, using the strict conditions of the GBIF matching

```bash
python species-list.tsv species-list.tsv --update --strict
```

### Python functions

When running the function inside Python, make sure the location is added to the PATH in order to enable the import of the function. 

Similar to the command line functionality, the python function `extract_species_information` reads an input file, request the information from GBIF and adds the required information from the mapping. 

```python
from gbif_species_name_extraction import extract_species_information
updated_tsv = extract_species_information("species-list.tsv", 
                                          output=None,
                                          api_terms=["usageKey", "scientificName", 
                                                     "canonicalName", "status", "rank", 
                                                     "matchType", "confidence"]
                                          update_cols=True,
                                          namecol=None, 
                                          kingdomcol=None,
                                          strict=True)
```
The arguments are directly corresponding to the arguments used in the command line functioning. Apart from a file, the input can be a Pandas dataframe as well (makes more sense in a python-development cycle. The function returns a Pandas dataframe with the updated information as well.

Apart from this function, some additional functions are available to the user.

#### API request to Gbif for species name info

Function `extract_gbif_species_names_info` provides a single request to the GBIF API in order to get information on the species from the backbone. Notice that this could be performed by the pygbif package[pygbif package](http://pygbif.readthedocs.io/en/latest/)  as well.    
    
    Parameters
    ----------
    species_name : str
        species name, preferably the Gbif proposed name
    kingdom : str
        kingdom of the species
    strict : boolean
        if true it (fuzzy) matches only the given name, but never a taxon in 
        the upper classification
    verbose:
        if true it shows alternative matches which were considered but then 
        rejected
        
#### Get the acceptedKey and acceptedScientificName for any usageKey of  GBIF

The function `extract_gbif_accepted_key` searches for an acceptedKey corresponding to the provided usage Key. If not available, an empty string is returned
    
    Parameters
    -----------
    usage_key : int
        usage_key as provided by GBIF for a specific species
    
    Returns
    --------
    acceptedKey : str
        key of the accepted name synonym
    acceptedScientificName : str
        scientific name of the accepted name synonym

### Examples

* To add the GBIF API information to an existing file (csv), saving as a new file
```bash
python gbif_species_name_extraction.py file_in.csv fileout.csv
```

* To add the GBIF API information to an existing file (csv), using the strict name matching from GBIF
```bash
python gbif_species_name_extraction.py file_in.csv fileout.csv --strict True
```    

* To add the GBIF API information to an existing file (csv), overwriting the same file
```bash
python gbif_species_name_extraction.py file.csv file.csv  
```

* To update the GBIF API information to an existing file (csv)
```bash
python gbif_species_name_extraction.py --update True file.csv file.csv
```    

* To update the GBIF API information to an existing file, defining the column to use for scientificName and kingdom
```bash
python gbif_species_name_extraction.py --namecol columnheader1 --kingdomcol columnheader2 --update True file1.tsv
file1.tsv
```

* Only add the terms status, rank and matchType as columns (acceptedKey is always added)
```bash
python gbif_species_name_extraction.py file.csv file.csv --api_terms status rank matchType   
```
