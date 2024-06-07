import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy
import preprocessor as pp
import helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = pp.preprocess(df, region_df)
df['Year'] = df['Year'].astype(str)


st.sidebar.title("Olympic Analysis")

user_menu = st.sidebar.radio(
    'Select an option', 
    ('Medal Tally', 'Overall Analysis', 'Countrywise Analysis', 'Athlete-wise analysis')
)



if user_menu == 'Medal Tally':
    st.sidebar.title("Medal Tally")
    years, countries = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Selected Year", years)
    selected_country = st.sidebar.selectbox("Selected Country", countries)
    medal_tally, Title = helper.fetch_medal_tally(df, selected_year, selected_country)

    st.title(Title)
    st.table(medal_tally)

if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    events = df['Event'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("### Editions")
        st.title(editions)
    with col2:
        st.write("### Cities")
        st.title(cities)
    with col3:
        st.write("### Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("### Athletes")
        st.title(athletes)
    with col2:
        st.write("### Nations")
        st.title(nations)
    with col3:
        st.write("### Events")
        st.title(events)


    st.title("Participating nations over Time")
    nat_ot = helper.column_over_time(df, 'region')
    fig = helper.print_graph(nat_ot, 'Year', color = 'b')
    st.pyplot(fig)

    st.title("Organized Events over Time")
    events_ot = helper.column_over_time(df, 'Event')
    fig = helper.print_graph(events_ot, 'Year', color = 'g')
    st.pyplot(fig)

    
    st.title("Organized Sports per Olympic year")
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    fig, ax = plt.subplots(figsize = (25,25))
    ax = sns.heatmap(x.pivot_table(index = 'Sport', columns = 'Year', values = 'Event', aggfunc = 'count').fillna(0).astype(int), annot = True) 
    st.pyplot(fig)
    
    st.title("Top Athletes")
    sports_list = helper.sports_list(df)
    selected_sport = st.selectbox("Select Sports", sports_list)
    top_athletes = helper.top_athletes(df, sport = selected_sport, country = None)
    st.table(top_athletes)


if user_menu == 'Countrywise Analysis':
    years, countries = helper.country_year_list(df)
    sel_country = st.sidebar.selectbox("Selected Country", countries)
    temp_df = helper.CwAnalyis(df, sel_country)

    if sel_country != 'Overall':
        st.title(sel_country + "'s performance in different sports across the years")
    else:
        st.title('All Sports conducted across the Years')
        st.write("#### Please select a country for analysis")
    fig, ax = plt.subplots(figsize = (20,20))
    ax = sns.heatmap(temp_df.pivot_table(index = 'Sport', columns = 'Year', values ='Medal', aggfunc = 'count').fillna(0).astype(int), annot = True)
    st.pyplot(fig)

    st.title("Top Athletes of " + sel_country)
    top_athletes = helper.top_athletes(df, sport = None, country = sel_country)
    st.table(top_athletes)

if user_menu == 'Athlete-wise analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot( [x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)


    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')