# Tools to handle bibliographic and other library related matters


## enRIScher: improve RIS bibliographic files

### Introduction

The main driver to develop the `enRIScher` module, was to automatically add the gdrive link of bibliographic references in an existing RIS file. Besides, some particularities about the import/export of RIS files in endnote can be handled as well (split of multiple URL's in a single UR field, provide default ST fields). 

### Aim

The enRIScher is a small library tool to handle and enrich RIS files.

### Installation

In order to use the `enRIScher`, the following dependencies are required (apart from Python itself, prefereably Python 3.5). These dependencies are all related to the google drive API calls (`INBOReferenceSearcher` class and registration process):

* `oauth2client`
* `httplib2` (installed as dependency of `oauth2client`)
* google `apiclient`: https://developers.google.com/api-client-library/python/

Installation can be done by with `conda` (conda-forge channel):
```
conda install oauth2client -c conda-forge
conda install google-api-python-client -c conda-forge
```

or with `pip`:
```
pip install oauth2client
pip install --upgrade google-api-python-client
```

### Google API registration

In order to work with the Google Drive API, you need to register your *application* (i.e. the command line interface tool). The easiest way to get started is to follow the steps of  [this](https://developers.google.com/drive/v3/web/quickstart/python) tutorial. 

During the tutorial, the location to write the API-json configuration is stored by default as: `yourhomedirectory/.credentials/drive-python-quickstart.json` by running the `quickstart.py` file (this is not the same as the `client_secret.json` file!). Make sure you know where the `drive-python-quickstart.json` is stored or change the location/name as you want.

### Functionality

The functionality is intended as a command line tool, as follows

```bash
>> python enRIScher.py --help
usage: enRIScher.py [-h] inputfile outputfile credentials

Enrich a given RIS file

positional arguments:
  inputfile    the relative path and filename to the original RIS file
  outputfile   the relative path and filename to the updated RIS file
  credentials  the relative path and filename to the google API credentials
               file

optional arguments:
  -h, --help   show this help message and exit
```

So, for example, consider the input file `library.ris`, the default location of the credentials file and requiring the new RIS file to be written into `updated_library.ris`, the command would be:

```bash
python enRIScher.py library.ris updated_library.ris ~/.credentials/drive-python-quickstart.json
```

Still, you're free to use the different classes and methods within Python itself as well. For example, to search for a specific file in the bibliographic teamdrive, use the `search_file` function:

```python
from enRIScher import INBOReferenceSearcher

library = INBOReferenceSearcher('drive-python-quickstart.json')
library.search_file("Anselin_2001_vogelnieuws2.pdf")
```

which returns:
```
('Anselin_2001_vogelnieuws2.pdf',
 'https://drive.google.com/open?id=0B7K_7SGyjAgMVlZtWXVnVDBmd3M')
```

More general queries are possible as well with the `query_references` method , explained [here](https://developers.google.com/drive/v3/web/search-parameters#fn1). For example, to find all files for which the file name contains `DNA` in the file name:

```
library.query_references("name contains 'DNA'")
```

In the next section, some more technicial information about the implementation is provided.

### Development

The utility provides 3 main classes: 

* `INBOReferenceSearcher`:  Class to search a team drive (default the bibliographic files drive) for files. It handles the gdrive authentification and provides a wrapper around the [google API to list/search files](https://developers.google.com/drive/v3/web/search-parameters).
* `Ris` : Class providing an iterator `entries` to loop over the individual entries in an RIS file and works as a context manager, handling the file open and closure:

  ```python
  with Ris(input_ris_file, 'r') as references:
      for entry in references.entries():
          # Do your thing on the individual entries
          print(entry)
  ```

* `RisRef`: A class to handle the individual entries. Contains the individual items as a list ad attribute `rislist`. It was chosen not to use a dictionary, to keep close to the raw file properties (lines,...). Utilities to handle RIS-entries are implemented on this level, using methods with the name convention `handle_*`. A `handle_all` method combines all the individual utility functions.
