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

https://developers.google.com/drive/v3/web/quickstart/python

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
