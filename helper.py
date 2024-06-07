import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def fetch_title(case, year, country):
    if case == 0:
        Title = "Overall Tally"
    elif case == 1:
        Title = country + "'s Overall Performance"
    elif case == 2:
        Title = "Medal Tally in " + str(year) + " Olympics"
    else:
        Title = country + "'s performnace in " + str(year) + " Olympics"
    
    return Title


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    case = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    elif year == 'Overall' and country != 'Overall':
        case = 1
        temp_df = medal_df[medal_df['region'] == country] 

    elif year != 'Overall' and country == 'Overall':
        case  = 2
        temp_df = medal_df[medal_df['Year'] == year]

    else : 
        case = 3
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]    

    if case == 1 : 
        medal_tally = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:    
        medal_tally = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()
    
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    Title = fetch_title(case, year, country)

    return medal_tally, Title


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')


    countries = np.unique(df['region'].dropna().values).tolist()
    countries.insert(0, 'Overall')

    return years, countries

def sports_list(df):
    Sports = df['Sport'].unique().tolist()
    Sports.sort()
    Sports.insert(0, 'Overall')
    return Sports



def column_over_time(df, col):
    required_df = df.drop_duplicates(['Year', col ])['Year'].value_counts().reset_index().sort_values('Year')
    return required_df

def print_graph(df, col1, col2 = 'count', xlabel = 'col1', ylabel = 'col2', color = 'r'):
    fig, ax = plt.subplots(figsize = (10,5))
    ax.plot(df[col1], df[col2], marker = "o", color = color)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation = 45)

    return fig

def top_athletes(df, sport, country):
    temp_df = df.dropna(subset = ['Medal'])
    medal_count = temp_df[['Name', 'region', 'Sport', 'Medal']]
    

    if sport != 'Overall' and country == None:
        temp_df = temp_df[temp_df['Sport'] == sport]
        medal_count = temp_df.groupby(['Name', 'region'])['Medal'].count().reset_index()

    elif country != 'Overall' and sport == None:
        temp_df = temp_df[temp_df['region'] == country]
        medal_count = temp_df.groupby(['Name', 'Sport'])['Medal'].count().reset_index()
    else:
        medal_count = medal_count.groupby(['Name', 'region', 'Sport'])['Medal'].count().reset_index()    

    top_athletes = medal_count.sort_values(by = 'Medal', ascending = False).head(10)
    return top_athletes

def CwAnalyis(df, country):
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]
    return temp_df