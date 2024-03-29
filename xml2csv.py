import lxml.etree as ET
import pandas as pd
import numpy as np
import time
import sys
import os

start_time = time.time()
diction = {}
file_name = sys.argv[1]

def main():
    chunk_size = check_file_size(file_name)
    xmlTreeRoot = create_xml_tree()
    iterate_XML_2_dict(xmlTreeRoot)
    dataFrame = create_dataframe()
    write_to_csv(dataFrame,chunk_size)

def check_file_size(file_name):
    file_size = os.path.getsize(file_name)/(1024*1024)
    print(f"File size: {file_size:.2f}MB")
    if file_size > 500:
        while True:
            try:
                chunks = int(input("Please enter number of how many files you want this file split into (e.g 2): "))
            except ValueError:
                print('***Please enter a valid integer***')
                continue
            break      
    else:
        chunks = 1
    return chunks

def create_xml_tree():
    ''' Creates XML tree ready to parse '''
    print('Creating XML tree')
    tree = ET.parse(file_name)
    root = tree.getroot()
    print('XML tree created')
    return root

def iterate_XML_2_dict(root):
    ''' Iterate through child object 
        and add tag and text to dictionary '''    
    print ('Adding values from XML > Dictionary')
    for child in root:
        for innerC in child:
            add_values_in_dict(diction, str(innerC.tag), str(innerC.text))
    print('Finished adding values to dictionary')
    print("--- %s seconds ---" % (time.time() - start_time))

def add_values_in_dict(dict, key, list_of_values):
    ''' Append multiple values to a key in 
        the given dictionary '''
    if key not in dict:
        dict[key] = list()
    if list_of_values == 'None':
        dict[key].append('')
    else:
        dict[key].append(list_of_values)
    return dict

def create_dataframe():
    ''' Creates dataframe using Pandas, 
        Created using the dictionary of lists'''
    df = pd.DataFrame(data=diction)
    df.fillna("",inplace=True)
    print('Finished loading dictionary into dataframe')
    print("--- %s seconds ---" % (time.time() - start_time))#
    return df

def write_to_csv(df, chunks):
    ''' Creates output folder in current path, 
        Checks if output folder exists before creating
        Will then check if file needs to be split
        Then will output file into CSV'''    
    existingPath = os.getcwd()
    newPath = os.getcwd() + '\output'
    try:
        os.mkdir(newPath)
    except OSError:
        print ("Successfully saved in directory: %s " % newPath)
    else:
        print ("Successfully created the directory %s " % newPath)
    os.chdir(newPath)
    #df.to_csv(os.path.basename(file_name) + '.csv',index = False,na_rep='')
    for idx, chunk in enumerate(np.array_split(df, chunks)):
        if chunks > 1:
            chunk.to_csv(f'{idx}' + os.path.basename(file_name) + '.csv', index=False)
        else:
            chunk.to_csv(os.path.basename(file_name) + '.csv', index=False)
    print(str(time.process_time()) + ' seconds taken to convert.')
    os.chdir(existingPath)

def output_csv(df):
    df.to_csv("output.csv",na_rep='', index=False)
    print("Total time taken: " + "--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
