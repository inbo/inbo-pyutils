#
# Library RIS bibliographic records update tool
#
# Author: Stijn Van Hoey
# INBO

from __future__ import print_function
import argparse
import os
import sys
import re

import httplib2
from oauth2client.file import Storage
from apiclient import discovery

"""
! ATTENTION !

Make sure to enable the google API by following 
[this](https://developers.google.com/drive/v3/web/quickstart/python) tutorial.
The file will create a credentials file from which following authentifications 
can be used.
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


TAG_PATTERN = "^[A-Z][A-Z0-9]  - "


class RisRef(object):

    def __init__(self, rislist):
        """"""
        self.rislist = rislist
        self.keywords = self._extract_keywords()

    def _extract_keywords(self):
        """get all the key-words from the rislist"""
        return [self.get_tag(line) if self.get_tag(line) else None for line in self.rislist]

    @staticmethod
    def is_tag(line):
        pattern = re.compile(TAG_PATTERN)
        return bool(pattern.match(line))

    def get_tag(self, line):
        """RIS file has always a setup of 'KW  - ', with the first two characters the tag"""
        if self.is_tag(line):
            return line[:2]
        else:
            return None

    def get_content(self, line):
        """RIS file has always a setup of 'KW  - ...', with the first 6 characters strictly defined"""
        if self.is_tag(line):
            return line[6:].strip()
        else:
            return None

    def handle_st(self):
        """if no ST field, add an empty st_field"""
        if "ST" not in self.keywords:
            # Provide the ST as an additional keyword
            self.rislist.insert(-1, 'ST  - \n')
            # Add ST to the keywords
            self.keywords.append('ST')

    def handle_ur(self):
        """split multiple URL on a single line to multiple line"""
        if 'UR' in self.keywords:
            ur_index = self.keywords.index('UR') +1
            while not self.is_tag(self.rislist[ur_index]):
                self.rislist[ur_index] = ''.join(['UR  - ', self.rislist[ur_index]])
                ur_index +=1

    def handle_gdrivelink(self, ris_matcher):
        """add a google drive link to the entry, after the L1 file statement"""

        if 'L1' in self.keywords:
            l1_index = self.keywords.index('L1')
            line = self.rislist[l1_index]

            filename = re.search("([^/&\\\]*?\.\S*)", line.rstrip()).group(0)

            name, url = ris_matcher.search_file(filename)
            if url:
                self.rislist.insert(l1_index + 1, "".join(["UR  - ", url, "\n"]))

    def handle_all(self, ris_matcher):
        self.handle_ur()
        self.handle_st()
        self.handle_gdrivelink(ris_matcher)


class Ris(object):

    START_TAG = 'TY'
    END_TAG = 'ER'
    PATTERN = '^[A-Z][A-Z0-9]  - '

    def __init__(self, file_name, mode='r'):
        self.file_name = file_name
        self.mode = mode
        self._current_entry = []

    def __enter__(self):
        self.file_object = open(self.file_name, self.mode)
        return self

    def __exit__(self, *args):
        self.file_object.close()

    def entries(self):
        """generator to loop all the entries in a RIS-file"""

        while True:
            current_line = self.file_object.readline()
            if not current_line:
                break

            #if not current_line == "\n": # skip empty lines
            self._current_entry.append(current_line)

            if current_line.startswith("ER"):
                yield RisRef(self._current_entry)
                self._current_entry = []


def update_RIS_file(input_ris_file, updated_ris_file, credentials_file):
    """Enrich an exising RIS file in order to update the database entries

    For a given RIS file, following actions are taken to enrich the file:
    - For a given set of URL's without the UR-keyword, provide the UR keyword
    - When no ST keyword is available, provide an empty ST keyword
    - For a given file name of a bibliographic entry (L1), provide an additional line with the corresponding google drive URI (UR)

    """
    ris_matcher = INBOReferenceSearcher(credentials_file)
    with Ris(input_ris_file, 'r') as risser:
        with open(updated_ris_file, 'w') as references_update:
            for entry in risser.entries():
                entry.handle_all(ris_matcher)
                references_update.writelines(entry.rislist)


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
    print('quickly grab a coffee :-)')
    update_RIS_file(args.inputfile, args.outputfile, args.credentials)
    print("...processing done, the updated file is available at ", args.outputfile)

if __name__ == "__main__":
    sys.exit(main())
