#
# Library RIS bibliographic records update tool
#
# Author: Stijn Van Hoey
# INBO

from __future__ import print_function
import httplib2
import argparse
import os
import sys
import re

from oauth2client.file import Storage
from apiclient import discovery

"""
! ATTENTION !

Make sure to enable the google API by running the `gdrive_account_setup.py`,
following [this](....TODO..) tutorial. The file will create a credentials file
in the home directory (config_file subfolder), from which credentials can be
used.
"""

class INBOReferenceSearcher(object):
    """
    This class provides the tools to interact with a Teamdrive and look for files and their corresponding URI. Both plain file name searches, as well as the google API query functionalities are supported.

    Example
    -------
    ris_matcher = INBOReferenceSearcher('credentials.json')
    # search for a specific file name:
    name, url = ris_matcher.search_file("Anselin_2001_vogelnieuws2.pdf")
    # search by a query (see: https://developers.google.com/drive/v3/web/search-parameters#fn1)
    ris_matcher.query_references("name contains 'DNA'")
    """

    def __init__(self, cred_file,
                 bibliographic_drive="0ACMs9qA33X6eUk9PVA"):
        """
        Within the given drive teamfolder, search for files and retrieve the
        corresponding URI for the file. Besides the `search_file` functionality,
        the more general query options for G-drive are applicable as well.

        Parameters
        -----------
        cred_file : str
            local json file containing the credentials for the API access to the gdrive. The file can be retrieved by running the `gdrive_account_setup.py` after creating a API token
            in your google account.
        bibliographic_drive : str
            hash of the Gdrive location to search for files. The easiest way to get these is by
            checking the last sectioin of the URL when opening the drive.
        """
        self.cred_file_location = cred_file
        self.drive_id = bibliographic_drive
        self.service = self._connection()

    def _connection(self):
        """using an credentials file, setup the gdrive connection as a service
        """
        storage = Storage(self.cred_file_location)
        credentials = storage.get()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)
        return service

    @staticmethod
    def _name_fixer(filename):
        """tweak a pdf file name to make it query-ready for the gdrive listing
        """
        return "".join(["name='", filename, "'"])

    def query_references(self, query):
        """search files on bibliographic team drive in google (or any other defined drive)

        To define the query, see https://developers.google.com/drive/v3/web/search-parameters#fn1 for detailed documentation.
        """
        response = self.service.files().list(q=query,
                                             teamDriveId=self.drive_id,
                                             corpora="teamDrive",
                                             includeTeamDriveItems=True,
                                             supportsTeamDrives=True).execute()
        return(response)

    @staticmethod
    def get_gdrive_url(file_id):
        """transform the file hash to the corresponding URL to open the file
        """
        return "".join(["https://drive.google.com/open?id=", file_id])

    def search_file(self, filename):
        """lookup specific file name in the defined team drive
        """
        response = self.query_references(self._name_fixer(filename))

        if response["incompleteSearch"]:
            raise Exception("Search not completed for file ", filename)

        if len(response["files"]) == 0:
            print("No match found for file ", filename)
            return filename, None
        elif len(response["files"]) > 1:
            print("Multiple matches found for file ", filename)
            file_ids = [self.get_gdrive_url(file_info['id']) for file_info in response.get('files', [])]
            return filename, file_ids
        else:
            return filename, self.get_gdrive_url(response['files'][0]['id'])


def update_RIS_file(input_ris_file, updated_ris_file, credentials_file):
    """Enrich an exising RIS file in order to update the database entries

    For a given RIS file, following actions are taken to enrich the file:
    - For a given file name of a bibliographic entry (L1), provide an additional line with the corresponding google drive URI (UR)
    -

    """
    ris_matcher = INBOReferenceSearcher(credentials_file)
    with open(input_ris_file, "r") as references:
        with open(updated_ris_file, "w") as references_update:
            for line in references.readlines():
                references_update.write(line)
                if line.find('L1') != -1:
                    filename = re.search("([^/&\\\]*?\.\S*)", line.rstrip()).group(0)
                    name, url = ris_matcher.search_file(filename)
                    print(filename, name, url)
                    if url:
                        references_update.write("".join(["UR  - ", url, "\n"]))

def main(argv=None):
    """
    Udate a given RIS file with additional information on the Gdrive location
    """
    parser = argparse.ArgumentParser(description="""Enrich a given RIS file""")

    parser.add_argument('inputfile', type=str,
                        help='the relative path and filename to the original RIS file')

    parser.add_argument('outputfile', action='store',
                        help='the relative path and filename to the updated RIS file')

    parser.add_argument('credentials', action='store',
                        help='the relative path and filename to the google API credentials file')

    args = parser.parse_args()

    print("Processing RIS file...")
    print(args)
    update_RIS_file(args.inputfile, args.outputfile, args.credentials)
    print("...processing done, the updated file is available at ", args.outputfile)

if __name__ == "__main__":
    sys.exit(main())
