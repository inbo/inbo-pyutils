# Tools to handle bibliographic and other library related matters


## enRIScher: improve RIS bibliographic files

### Introduction

The main driver to develop the `enRIScher` module, was to automatically add the gdrive link of bibliographic references in an existing RIS file. Besides, some particularities about the import/export of RIS files in endnote can be handled as well (split of multiple URL's in a single UR field, provide default ST fields). 

### Aim

The enRIScher is a small library tool to handle and enrich RIS files.

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
