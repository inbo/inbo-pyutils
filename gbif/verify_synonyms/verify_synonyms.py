
import sys
import textwrap
import argparse

import pandas as pd

# Way to call script:

def verify_synonym(input_file, output_file, synonym_file,
                   usagekeycol='gbifapi_usageKey', 
                   acceptedkeycol='gbifapi_acceptedKey', 
                   taxonomicstatuscol='gbifapi_status',
                   outputcol='nameMatchValidation'):
    """verify if more information on the synonyms is already present
    Find out which of the synonyms were already registered as defined by the 
    synonym_file, by checking the match between the usageKey AND acceptedKey
    as provided by GBIF. When a match is found, the status as registered in the
    synonym-file is provided.

    Parameters:
    --------
    input_file: str (filepath) | pd.DataFrame
        input file to check the synonym values or pandas Dataframe
    output_file: str (filepath) | None
        output file to write result, if None, no output file will be created
    synonym_file: str
        relatie path to the synonym file for the verification
    usagekeycol: str (default: gbifapi_usageKey)
        column name with the usagekey for input_file 
    acceptedkeycol: str (default: gbifapi_acceptedKey)
        column name with the acceptedKey for input_file  
    taxonomicstatuscol: str (default: gbif_apistatus)
        column name with the API status of GBIF for input_file, NOT  status
    outputcol: str
        column name to put the remarks of the verification of the input file
        
    Remarks:
    --------
    For the synonym_file, the names of the usagekey, acceptedkey and status
    columns are fixed and should be equal to respectively `gbifapi_usageKey`,  
    `gbifapi_acceptedKey` and 'status'
    """
    
    if taxonomicstatuscol == "status":
        raise Exception('Change name of the status column of your input file')
    
    if isinstance(input_file, str):
        # Reading in the files (csv or tsv)
        if input_file.endswith('tsv'):
            delimiter = '\t'
        else:
            delimiter = ','
        input_file = pd.read_csv(input_file, sep=delimiter, 
                                encoding='utf-8', dtype=object)  
    elif isinstance(input_file, pd.DataFrame):
        delimiter = ',' # Patch: set a delimiter for the output file
        input_file = input_file.copy()
    else:
        raise Exception('Input datatype not supported, use either str or a \
                            pandas DataFrame')
    
    # read the synonyms file    
    synonyms = pd.read_csv(synonym_file, sep='\t', dtype=object)
    
    #extract useful columns from synonym file (expected to be fixed)
    synonyms_subset = synonyms[["gbifapi_usageKey", "gbifapi_acceptedKey", "status"]]
    
    # Check the matches by doing a join of the inputfile with the synonym
    verified = pd.merge(input_file, synonyms_subset, how='left',
                        left_on=[usagekeycol, acceptedkeycol], 
                        right_on=["gbifapi_usageKey", "gbifapi_acceptedKey"])
    
    # overwrite for SYNONYM values when already present
    if outputcol in verified.columns:
        verified.loc[verified[taxonomicstatuscol] == "SYNONYM", outputcol] = \
            verified.loc[verified[taxonomicstatuscol] == "SYNONYM", 'status']
        verified = verified.drop('status', axis=1)
    else:
        verified = verified.rename(columns={'status' : outputcol})
        
    if (output != None) & isinstance(output,str):
        verified.to_csv(output_file, sep=delimiter, index=False, 
                            encoding='utf-8')
    return verified


def main(argv=None):
    """
    Use usagekeycol and acceptedkeycol to lookup a match in the synonymlist

    * If match found and status = ok:
        populate statuscol with: ok: SYNONYM verified
    * If match found and status <> ok:
        populate statuscol with: verify: SYNONYM <status>
    * If no match found: 
        do nothing    
    """    
    parser = argparse.ArgumentParser(description="""Lookup a match in the 
        synonymlist. If match and status is ok, the record is enlisted as 
        SYNONYM verified; if match but status is not ok, the record is 
        provided of a verify status. If no match is found, nothing is done.
        """)    
    
    parser.add_argument('input_file', type=str,
                        help='the relative path and filename containing the usage and acceptedkey col')
                       
    parser.add_argument('output_file', action='store', default=None, 
                        help='output file name, can be same as input')              
    
    parser.add_argument('--synonym_file', type=str,
                        action='store', default=None, 
                        help='relative path and filename to the file containing the synonym status information')                                            

    parser.add_argument('--usagekeycol', type=str,
                        action='store', default='gbifapi_usageKey', 
                        help='column name of the input file containing the gbif usage keys (default when not provided: `gbifapi_usageKey`)')                                            

    parser.add_argument('--acceptedkeycol', type=str,
                        action='store', default='gbifapi_acceptedKey', 
                        help='column name of the input file containing the gbif accepted keys (default when not provided: `gbifapi_acceptedKey`)')  

    parser.add_argument('--taxonomicstatuscol', type=str,
                        action='store', default='gbifapi_status', 
                        help='column name of the input file containing the gbif taxonomic matchin status information, e.g. SYNONYM (default when not provided: `gbifapi_status`)')                        

    parser.add_argument('--outputcol', type=str,
                        action='store', default='nameMatchValidation', 
                        help='column name of the output file to provide the information about the synonym status (default when not provided: `nameMatchValidation`)')                        

    args = parser.parse_args()    
    
    print("Verification of the synonym names...")
    print(textwrap.dedent("""\
                          Using {} as input file and searching matches
                          with the synonmys enlisted in {}
                          """.format(args.input_file, 
                                     args.synonym_file)))
    print(textwrap.dedent("""\
                          Columns of usage_key and accepted_key as provided by
                          gbif in the input file are named respectively {} 
                          and {}. The columns with the taxonomicstatus 
                          (SYNONYM,...) is named {}
                          """.format(args.usagekeycol, 
                                     args.acceptedkeycol,
                                     args.taxonomicstatuscol)))
    print(textwrap.dedent("""\
                          Writing verification information to column {}
                          """.format(args.outputcol)))
    verify_synonym(args.input_file, args.output_file,
                   args.synonym_file,
                   args.usagekeycol,
                   args.acceptedkeycol,
                   args.taxonomicstatuscol,
                   args.outputcol
                   ) 
    print("".join(["saving to file", args.output_file, "...done!"]))

if __name__ == "__main__":
    sys.exit(main())    
