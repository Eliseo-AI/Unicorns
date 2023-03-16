import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import folium
from streamlit_folium import folium_static
from collections import Counter

# Load your data as a Pandas DataFrame (replace "your_data.csv" with your actual file)
data = pd.read_csv("data/unicorns_2022.csv")

# Clean selected_investors column
data['selected_investors'] = data['selected_investors'].apply(lambda x: [i.strip() for i in x.split(',')])

st.title("Data Analysis")

# Horizontal line graph by country
st.header("Horizontal Line Graph by Country")
countries = data['country'].unique()
selected_countries = st.multiselect("Select countries:", countries, default=countries)

filtered_data = data[data['country'].isin(selected_countries)]
agg_data = filtered_data.groupby(['country', 'date_joined']).agg({'value': 'sum'}).reset_index()

fig1 = px.line(agg_data, x='date_joined', y='value', color='country', orientation='h')
st.plotly_chart(fig1)

# Bubble graph by industry
st.header("Bubble Graph by Industry")
industry_data = data.groupby('industry').agg({'value': 'sum', 'unicorn': 'count'}).reset_index()
fig2 = px.scatter(industry_data, x='unicorn', y='value', size='value', color='industry', text='industry')
fig2.add_hline(y=industry_data['value'].mean())
fig2.add_vline(x=industry_data['unicorn'].mean())
st.plotly_chart(fig2)

# Boxplot graph
st.header("Boxplot Graph")
countries_to_compare = st.multiselect("Select countries to compare:", countries, default=countries[:3])
boxplot_data = data[data['country'].isin(countries_to_compare)]
fig3 = px.box(boxplot_data, x='country', y='value')
st.plotly_chart(fig3)

# Map visualization
st.header("Map Visualization")
m = folium.Map(location=[37.7749, -122.4194], zoom_start=4)

for index, row in data.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        radius=row['value'] * 10,
        color=row['date_joined'],
        popup=f"{row['unicorn']} - {row['value']} trillion - {row['industry']}",
        fill=True
    ).add_to(m)

folium_static(m)

# Investor analysis
st.header("Investor Analysis")
investors_counter = Counter([investor for investors in data['selected_investors'] for investor in investors])
range_slider = st.slider("Select range:", min_value=0, max_value=max(investors_counter.values()), value=(0, max(investors_counter.values())))
investors_filtered = {k: v for k, v in investors_counter.items() if range_slider[0] <= v <= range_slider[1]}
fig4 = px.bar(pd.DataFrame.from_dict(investors_filtered, orient='index', columns=['count']).reset_index(), x='count', y='index', labels={'index': 'Investor'})
st.plotly_chart(fig4)

investor_choice = st.selectbox("Select an investor:", list(investors_filtered.keys()))
investor_companies = data[data['selected_investors'].apply(lambda x: investor_choice in x)][['unicorn', 'value', 'industry']]
st.write(investor_companies)

# Bubble map with animation
st.header("Bubble Map with Animation")
animated_data = data.groupby(['id_city', 'lat', 'lng', 'city', 'population', 'date_joined']).agg({'value': 'sum'}).reset_index()
fig5 = px.scatter_geo(animated_data, lat='lat', lon='lng', size='value', color='id_city', animation_frame='date_joined', hover_name='city', hover_data=['id_city', 'population', 'value'], projection='natural earth')
st.plotly_chart(fig5)
