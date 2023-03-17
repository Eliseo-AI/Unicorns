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

# Create a scatter plot
fig = px.scatter(data, x="value", y="year", color="country", 
                 log_x=True, size="value", hover_name="unicorn",
                 symbol="industry")

# Customize the layout
fig.update_layout(
    title="Unicorn Companies by Country",
    xaxis_title="Value (in trillions of dollars)",
    yaxis_title="Year",
    legend_title="Country",
    hovermode="closest",
    margin=dict(l=0, r=0, t=50, b=0),
    height=600,
    width=800
)

# Add a slider to select the year
year = st.slider("Year", min_value=data['year'].min(), 
                 max_value=data['year'].max(), value=data['year'].min())

# Add a multiselect to select the countries to display
countries = st.multiselect("Select countries", options=data['country'].unique(), default=data['country'].unique())

# Filter the data by year and country
data_filtered = data[(data['year'] == year) & (data['country'].isin(countries))]

# Display the plot
st.plotly_chart(fig.update_traces(marker_opacity=0.8, marker_line_width=0.2, hovertemplate="<b>%{hovertext}</b><br>Country: %{customdata}<br>Value: %{x:.2f} trillion dollars<br>Industry: %{symbol}"), use_container_width=True)

# Show the selected countries
st.write("Selected countries:", countries)

# Show the filtered data
st.write("Data for year", year, "and selected countries:")
st.write(data_filtered)

# Add a multiselect to select the countries to display
countries = st.multiselect("Select countries", options=data['country'].unique(), default=data['country'].unique())

# Filter the data by year and country
data_filtered = data_year[(data_year['year'] >= year_range[0]) & (data_year['year'] <= year_range[1]) & (data_year['country'].isin(countries))]

# Display the plot
st.plotly_chart(fig.update_traces(marker_opacity=0.8, marker_line_width=0.2), use_container_width=True)

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
fig3 = px.box(boxplot_data, x='country', y='value', color='country')
st.plotly_chart(fig3)

# Map visualization
st.header("Map Visualization")
m = folium.Map(location=[37.7749, -122.4194], zoom_start=1.5)

for index, row in data.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        radius=row['value'] * 1,
        color=row['country'],
        popup=f"{row['country']} -{row['unicorn']} - {row['value']} - {row['industry']}", 
        fill=True
    ).add_to(m)

folium_static(m)

# Investor analysis
st.header("Investor Analysis")
investors_counter = Counter([investor for investors in data['selected_investors'] for investor in investors])
range_slider = st.slider("Select range:", min_value=0, max_value=max(investors_counter.values()), value=(0, max(investors_counter.values())))
investors_filtered = {k: v for k, v in investors_counter.items() if range_slider[0] <= v <= range_slider[1]}
fig4 = px.bar(pd.DataFrame.from_dict(investors_filtered, orient='index', columns=['count']).reset_index(), x='count',
              y='index', labels={'count':'Total Unicorns','index': 'Fund Investor'})
st.plotly_chart(fig4)

investor_choice = st.selectbox("Select an investor:", list(investors_filtered.keys()))
investor_companies = data[data['selected_investors'].apply(lambda x: investor_choice in x)][['ranking_companies','unicorn', 'value', 'industry','country']]
st.write(investor_companies)

# Bubble map with animation
st.header("Bubble Map with Animation")
animated_data = data.groupby(['id_city', 'lat', 'lng', 'city', 'population', 'date_joined']).agg({'value': 'sum'}).reset_index()
fig5 = px.scatter_geo(animated_data, lat='lat', lon='lng', size= 'value', color='country', animation_frame='date_joined', hover_name='city', hover_data=['id_city', 'population', 'value'], projection='natural earth')
st.plotly_chart(fig5)
