import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

header = st.container()
dataset = st.container()
features = st.container()
model_trainig = st.container()

with header:
    st.title('Welcome')
    st.text('This is the Dashboard of the Unicorn Companies')

with dataset:
    st.header('Dataset')
    st.text('The dateset include the total of Unicorns companies around the world top 10 Unicorns by Valuation in US$')
   
    data_unicorn = pd.read_csv('data/unicorns_2022.csv', sep=',')
    st.write(data_unicorn.head(10))
  
    st.subheader('Total Valuation of Unicorns by Country')
    countries = pd.DataFrame(data_unicorn.groupby(["country"])["value"].sum()).head(50)
    st.bar_chart(data=countries)
    
    st.subheader('Total Valuation by Industry')
    industry_value = pd.DataFrame(data_unicorn.groupby(["industry"])["value"].sum()).head(50)
    st.bar_chart(data=industry_value)
        
    st.subheader('Choose the Best combination between date and Industry')
    
    data_unicorn['date_joined'] = pd.to_datetime(data_unicorn['date_joined']).dt.strftime('%Y-%m-%d')
    
    industry_options = data_unicorn['industry'].unique().tolist()
    year_option = pd.DatetimeIndex(data_unicorn['date_joined']).unique().tolist()
        
    date = st.selectbox("Which date would you like to see", year_option,100)
    industry_u = st.multiselect("Which industry would you like to see", industry_options, ['Fintech'])
    
    data_unicorn = data_unicorn[data_unicorn['industry'].isin(industry_u)]
    data_unicorn = data_unicorn[data_unicorn['date_joined']==date]
    
    fig = px.bar(data_unicorn,x="industry",y="value",color="industry", range_y=[0,500])
    
    fig.update_layout(width=800)
    
    st.write(fig)
    
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": 37.76,
        "longitude": -122.4,
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data =data_unicorn[['value','lat','lng']],
        get_position=['lng','lat'],
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
        pdk.Layer(
             'ScatterplotLayer',
             data= data_unicorn[['value','lat','lng']],
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
    ],
))    
   
