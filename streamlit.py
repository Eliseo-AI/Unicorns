import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk


st.title("Unicorns Companies")
st.markdown("This application is a Streamlit dashboard that can be used "
"to analize unicorn companies around the world"
"")
@st.cache(persist=True)

data = pd.to_read('data/unicorns_2022.csv', sep = ',')

st.header("Where are the most valuable Unicorn Companies")
injured_people = st.slider("value of companies in US$ Dollars", 0, 150)
st.map(data.query("value >= @value")[["lat","lng"]].dropna(how="any"))

st.header("How many unicorns per year")
hour = st.slider("Hour to look at", 2011, 2022)
data = data[data['date_joined'].dt.year == year]

st.markdown("new unicorns between %i:00 and %i:00" % (year, (year + 1) % 2022))
midpoint = (np.average(data['lat']),np.average(data['lng']))


st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "lat": midpoint[0],
        "lng": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data =data[['date_joined','lat','lng']],
        get_position=['lng','lat'],
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))


if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)

