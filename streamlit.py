import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import altair as alt
from keplergl import KeplerGl
import json

@st.cache_data
def load_data():
    data = pd.read_csv('data/unicorns_2022.csv')
    data['date_joined'] = pd.to_datetime(data['date_joined'])
    data['year'] = data['date_joined'].dt.year
    data['selected_investors'] = data['selected_investors'].apply(lambda x: [i.strip() for i in x.split(',')])
    return data

data = load_data()
# Create a sidebar for user input:
st.sidebar.title("User Input")
selected_countries = st.sidebar.multiselect("Select countries", data['country'].unique(), default=['Country1', 'Country2'])
# Create the scatter plot:
scatter_data = data[data['country'].isin(selected_countries)]

scatter = alt.Chart(scatter_data).mark_circle().encode(
    alt.X('value', title='Value Range'),
    alt.Y('year', title='Year'),
    alt.Color('country', legend=alt.Legend(title="Countries")),
    tooltip=['unicorn', 'country', 'year']
).interactive()

st.altair_chart(scatter, use_container_width=True)
# Create the bubble chart:
bubble_data = data.groupby('industry').agg({'unicorn': 'count', 'value': 'sum'}).reset_index()

bubble = alt.Chart(bubble_data).mark_circle().encode(
    alt.X('unicorn', title='Number of Companies by Industry'),
    alt.Y('value', title='Total Value by Industry'),
    alt.Color('industry', legend=alt.Legend(title="Industries")),
    tooltip=['industry', 'unicorn', 'value']
).interactive()

st.altair_chart(bubble, use_container_width=True)
# Create the boxplot chart:
boxplot_data = data[data['country'].isin(selected_countries)]

boxplot = alt.Chart(boxplot_data).mark_boxplot().encode(
    alt.X('country', title='Country'),
    alt.Y('value', title='Value Range'),
    alt.Color('country', legend=alt.Legend(title="Countries")),
    tooltip=['unicorn', 'country', 'value']
).interactive()

st.altair_chart(boxplot, use_container_width=True)
# Create the 3D map:
map_data = data[['unicorn', 'industry', 'lat', 'lng', 'value', 'year']].copy()
map_data.columns = ['name', 'industry', 'latitude', 'longitude', 'elevation', 'year']

view_state = pdk.ViewState(latitude=37.7749, longitude=-122.4194, zoom=10, pitch=50)

map_layer = pdk.Layer(
    "HexagonLayer",
    data=map_data,
    get_position=["longitude", "latitude"],
    get_elevation="elevation",
    elevation_scale=1000,
    extruded=True,
    pickable=True,
    coverage=1,
    get_fill_color=["year * 10", "year * 10", "year * 10", 255],
)

map = pdk.Deck(map_style="mapbox://styles/mapbox/light-v9", initial_view_state=view_state, layers=[map_layer], tooltip={"text": "{name}\nValue: {elevation}\nIndustry: {industry}"})

st.pydeck_chart(map)
