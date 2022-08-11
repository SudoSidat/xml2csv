import lxml.etree as ET
import pandas as pd
import numpy as np
import time

start_time = time.time()
diction = {}

def main():
    xmlTreeRoot = create_xml_tree()
    iterate_XML_2_dict(xmlTreeRoot)
    dataFrame = create_dataframe()
    output_csv(dataFrame)

def create_xml_tree():
    ''' Creates XML tree ready to parse '''
    print('Creating XML tree')
    tree = ET.parse('test.xml')
    root = tree.getroot()
    print('XML tree created')
    return root

def iterate_XML_2_dict(root):
    ''' Iterate through child object 
        and add tag and text to dictionary '''    
    print ('Start adding values from XML > Dictionary')
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

def output_csv(df):
    #for idx, chunk in enumerate(np.array_split(df, 2)):
        #chunk.to_csv(f'output{idx}.csv')
    df.to_csv("output.csv",na_rep='', index=False)
    print("Total time taken: " + "--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
