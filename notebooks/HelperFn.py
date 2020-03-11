import numpy as np
import matplotlib.pyplot as plt

def colpercent(df):
    '''
    helper function to print columns with missing and the percentage missingness:
    '''
    print("Total NaN in Dataframe: " , df.isnull().sum().sum())
    print("Percent Missingness in Dataframe: ", 100*df.isnull().sum().sum()/(len(df.index)*len(df.columns)))
    print('-'*55)
    percentnulldf = df.isnull().sum()/(df.isnull().sum()+df.notna().sum())
    print("Percent Missingness by Columns:")
    print(100*percentnulldf[percentnulldf>0].sort_values(ascending=False))

def colpercount(df):
    '''
    printout to help view levels within features with missingness
    '''
    percentnulldf = df.isnull().sum()/(df.isnull().sum()+df.notna().sum())
    percent_ordered_df=percentnulldf[percentnulldf>0].sort_values(ascending=False)
    for i in range(len(percent_ordered_df)):
        print(percent_ordered_df.index[i])
        print('-'*15)
        print(train[percent_ordered_df.index[i]].value_counts())
        print('-'*55)

def zeroper(df, value):
    '''
    helper function to print out percentage of zeroes by column
    '''
    l=[]
    columns=[]
    for i in range(len(df.columns)):
        if 0 in df[df.columns[i]].value_counts():
            if 100*df[df.columns[i]].value_counts().loc[0]/len(df[df.columns[i]])>value:
                l.append((df.columns[i], 100*df[df.columns[i]].value_counts().loc[0]/len(df[df.columns[i]])))
            else:
                pass
        else:
            pass
    print(len(l))    
    print('-'*55)
    for j in range(len(l)):
        columns.append(l[j][0])
        print('Percent of zeroes: ', l[j])
        print('-'*55)
    print(columns)
    return columns

def data_eval(df):
    '''
    helper functions to characterize missingness by row and column
    '''
    for i in range(len(df.columns)):
        print('-'*50)
        print('Column Name: ', df.columns[i])
        if (df[df.columns[i]].dtypes == 'float64' or df[df.columns[i]].dtypes == 'int64') \
        and df[df.columns[i]][df[df.columns[i]]<0].count()>0:
            print('Number of negatives: ', df[df.columns[i]][df[df.columns[i]]<0].count())
        if df[df.columns[i]][df[df.columns[i]]=='None'].count() > 0:
            print('Number of None strings: ', df[df.columns[i]][df[df.columns[i]]=='None'].count())
        if df[df.columns[i]][df[df.columns[i]]==''].count() > 0:
            print('Number of empty strings: ', df[df.columns[i]][df[df.columns[i]]==''].count())
        else:
            print('Column ' + str(i) + ' has no negatives, empty strings or Nones')

def row_na_list(df, value):
    '''
    generates list of percentage missingness by row
    '''
    l=[]
    for i in range(len(df.index)) :
        if df.iloc[i].isnull().sum() > value:
            l.append([i, df.iloc[i].isnull().sum()])
    return l

def index_retrieve(df, value, measure):
    '''
    helper function to retrieve row and column index labels for correlation matrix values for greater than value when value>0 \ 
    and less than value when value<0. Prints out the values that correspond to those indices
    '''
    poslist = list()
    # Get bool dataframe with True at positions where the given value exists and filter out on-diagonal elements
    if measure == 'spearman':
        if value>0:
            result = df.corr(method = measure)[df.corr(method = measure)!=1][df.corr(method = measure)>value].isna().isin([value])
        if value<0:
            result = df.corr(method = measure)[df.corr(method = measure)!=1][df.corr(method = measure)<value].isna().isin([value])
        else:
            pass
    elif measure == 'pearson':
        if value>0:
            result = df.corr(method = measure)[df.corr(method = measure)!=1][df.corr(method = measure)>value].isna().isin([value])
        elif value<0:
            result = df.corr(method = measure)[df.corr(method = measure)!=1][df.corr(method = measure)<value].isna().isin([value])
        else:
            pass
    # Get list of columns that contains the value
    series = result.any()
    columnNames = list(series[series == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            poslist.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    if value > 0:
        print('Number of correlations with value greater than ' + str(value) + ': ' + str(len(poslist)))
    if value < 0:
        print('Number of correlations with value less than ' + str(value) + ': ' + str(len(poslist)))
    else:
        pass
    for i in range(len(poslist)):
        print('-'*40)
        print('index labels: ', poslist[i][0], poslist[i][1])
        print('value at index: ', df.corr().loc[poslist[i]])
    return poslist