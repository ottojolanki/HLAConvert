#HLAConvert version 0.01 by Otto Jolanki
#otaljo@gmail.com#python 2.76, pandas 0.12.0-1, numpy 1.7.1-2

from pandas import Series, DataFrame  
import pandas as pd                     
import re    
import numpy as np
import sys
#remove_asterisks is used for removing asterisks from the original format of the datafile
def remove_asterisks(value):
    if type(value)==str:
        return re.sub('[\*]','',value)
#remove_names is for cleaning up the reference file no.2
def remove_names(value):
    return re.sub('^\w+\*', '', value) 
#splitframe for separating numbers and letters in the data part of the original datafile
def splitframe(value):
    return value.split(':')
    
# returns a list of possible tokens
def get_possible_tokens(num, value):
    try:
        tokens = kirjainnrosarja[value].split('/')
    except KeyError:
        tokens = [num + ':' + value]
    else:
        for t in tokens:
            if len(t) == 2:
                tokens[tokens.index(t)] = '%s:%s' % (num, t)
    return tokens
#checks using the reference if a possible token is actually valid
def valid_token(token,columnname):
    for jono in refsarja[columnname].values:
        if jono.startswith(token):
            return True
    return False
#arg1=sys.argv[1]
#arg2=sys.argv[2]
#arg3=sys.argv[3]
#arg4=sys.argv[4]
#First we read in the filenames needed (commented out for testing)
#datafile=pd.read_table(sys.argv[1]) #the original data goes here
#kirjainnumero=pd.read_table(sys.argv[2])#the reference file no.1
#yleisreferenssi=pd.read_table(sys.argv[3])#the reference file no.2
datafile=pd.read_csv(sys.argv[1])
kirjainnumero=pd.read_table(sys.argv[2])  #the reference file goes here
yleisreferenssi=pd.read_table(sys.argv[3])#the final reference file

#Next is just munging the datafile, and the references to format we need for actually calculating something.
#First make the ID column of the datafile into actual ID, and not a column of data, and get rid of the data
#formatted column of the ID column from the datafile, and some other changes that are needed using the 
#functions defined above.
datafile.index=datafile['ID'].values
datafile=datafile.drop('ID', axis=1)
datafile=datafile.applymap(remove_asterisks)
#We replace missing values denoted by '*X' in the original .csv given by filling them from the cell to the left 
datafile=datafile.replace(to_replace='X', value=np.nan)
datafile=datafile.fillna(method='ffill', axis=1)
#Get the relevant part of the reference file 1, and make it appropriate for further use
refsarja=Series(np.array(yleisreferenssi['IMGT/HLA 3.9.0 Allele Name']),index=np.array(yleisreferenssi['Locus']))
refsarja=refsarja.map(remove_names)
#As munging procedure we create a series with appropriate indexing to prevent looping and difficulties in future
kirjainnrosarja=Series(np.array(kirjainnumero['SUBTYPE']),index=np.array(kirjainnumero['CODE']))
#Split the values in original data 
datafile=datafile.applymap(splitframe)
#After getting the data read, and in appropriate format, we need to take care of using the correct Loci.
#We do this by splitting the column names(see requirements for the column names in the original datafile)
def get_loci(dataframe):
    lista=[]
    for value in dataframe.columns.values:
        lista.extend(value.split(':')[0])
    return lista
result=pd.DataFrame(index=datafile.index)
for column in datafile.columns:
    lah=[]
    for num, value in datafile[column]:
        tokens=get_possible_tokens(num,value)
        valid_tokens=[t for t in tokens if valid_token(t,column.split(':')[0])]
        x=','.join(valid_tokens) #modify this to format output cells
        lah.append(x)
    result[column+'_matches']=lah    

result.to_csv(sys.argv[4])   







