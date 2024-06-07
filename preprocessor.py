import pandas as pd


def preprocess(df, region_df):

    #filtering for Summer Season only
    df = df[df['Season'] == 'Summer']
    #merging df and region_Df for country names
    df = df.merge(region_df, on = 'NOC', how= "left")
    #dropping duplicates
    df.drop_duplicates(inplace = True)
    #one-hot-encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis = 1)
    return df