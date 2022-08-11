import lxml.etree as ET
import pandas as pd
import numpy as np
import time

start_time = time.time()

print('Creating XML tree')
tree = ET.parse('rent.transactions20220811.xml')
root = tree.getroot()
diction = {}

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
print("--- %s seconds ---" % (time.time() - start_time))

print ('Start adding values from XML > Dictionary')
for child in root:
    for innerC in child:
        add_values_in_dict(diction, str(innerC.tag), str(innerC.text))
print('Finished adding values to dictionary')
print("--- %s seconds ---" % (time.time() - start_time))

df = pd.DataFrame(data=diction)
print('Finished loading dictionary into dataframe')
print("--- %s seconds ---" % (time.time() - start_time))

df.fillna("",inplace=True)
print('Finished replacing blanks')
print("--- %s seconds ---" % (time.time() - start_time))


#for idx, chunk in enumerate(np.array_split(df, 2)):
    #chunk.to_csv(f'output{idx}.csv')
df.to_csv("output.csv",na_rep='', index=False)
print("--- %s seconds ---" % (time.time() - start_time))

