import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import folium
from streamlit_folium import folium_static
from collections import Counter

st.set_page_config(
    page_title="Dashboard About Unicorn Companies",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded",
)
data = pd.read_csv("data/unicorns_2022.csv")

# Clean selected_investors column
data['selected_investors'] = data['selected_investors'].apply(lambda x: [i.strip() for i in x.split(',')])

st.title("Data Analysis")
with st.beta_expander("Explanation & Tips"):
     st.markdown(""" Analysis of All Unicorn Companies around the world in 2022, the information include the Market-Value, Industry and Country \n
     1. US$1 Billion or more as a Unicorn, 
     2. US$10 Billion as a Decacorn,
     3. US$100 Billion as a Hectatorn.""")

# Scatter Plot Graph by Country
st.subheader("Scatter Plot Graph by Country")
countries = data['country'].unique()
selected_countries = st.multiselect("Select countries:", countries, default=countries[:2])
filtered_data = data[data['country'].isin(selected_countries)]
agg_data = filtered_data.groupby(['country', 'year']).agg({'value': 'sum'}).reset_index()
fig1 = px.scatter(agg_data, x='year', y='value', color='country')
st.plotly_chart(fig1)

# Bubble graph by industry
st.subheader("Bubble Graph by Industry")
industry_data = data.groupby('industry').agg({'value': 'sum', 'unicorn': 'count'}).reset_index()
fig2 = px.scatter(industry_data, x='unicorn', y='value', size='value', color='industry', text='industry')
fig2.add_hline(y=industry_data['value'].mean())
fig2.add_vline(x=industry_data['unicorn'].mean())
st.plotly_chart(fig2)

# Boxplot graph
st.subheader("Boxplot Graph")
countries_to_compare = st.multiselect("Select countries to compare:", countries, default=countries[:2])
boxplot_data = data[data['country'].isin(countries_to_compare)]
fig3 = px.box(boxplot_data, x='country', y='value', color='country')
st.plotly_chart(fig3)

# Map visualization
st.subheader("Map Visualization")
m = folium.Map(location=[37.7749, -122.4194], zoom_start=8)
for index, row in data.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        radius=row['value'] ,
        color=row['year'],
        popup=f"{row['city']}-{row['unicorn']} - {row['value']}$B - {row['industry']}",
        fill=True
    ).add_to(m)
folium_static(m)

# Investor analysis
st.subheader("Investor Analysis")
investors_counter = Counter([investor for investors in data['selected_investors'] for investor in investors])
range_slider = st.slider("Select range:", min_value=0, max_value=max(investors_counter.values()), value=(0, max(investors_counter.values())))
investors_filtered = {k: v for k, v in investors_counter.items() if range_slider[0] <= v <= range_slider[1]}
#fig4 = px.bar(pd.DataFrame.from_dict(investors_filtered, orient='index', columns=['count']).reset_index(), x='count', y='index', labels={'index': 'Investor'})
top_investors = dict(sorted(investors_filtered.items(), key=lambda x: x[1], reverse=True)[:8])
df = pd.DataFrame({'Investor': list(top_investors.keys()), 'Count': list(top_investors.values()), 'Fund': list(top_investors.keys())})
fig4 = px.bar(df, x='Count', y='Investor', color='Fund', orientation='h', text='Investor')
fig4.update_layout(
    title="Investor Analysis",
    xaxis_title="Investor Count",
    yaxis_title="Investor",
    bargap=0.1
    )
st.plotly_chart(fig4)

# Fund Selection, comparison and Analysis 
st.subheader("Compare the funds")
with st.beta_expander("Explanation & Tips"):
     st.markdown(""" Select the Fund \n
     1. US$1 Billion or more as a Unicorn, 
     2. US$10 Billion as a Decacorn,
     3. US$100 Billion as a Hectatorn.""")
investor_choice = st.selectbox("Select an investor:", list(investors_filtered.keys()))
investor_companies = data[data['selected_investors'].apply(lambda x: investor_choice in x)][['ranking_companies','unicorn', 'value', 'industry','country']]
investor_companies = investor_companies.rename(columns={'ranking_companies': 'Ranking', 'unicorn': 'Company'})
investor_companies.index = range(1, len(investor_companies) + 1)
col1, col2 = st.beta_columns(2)

# Display the table in the left column
col1.write(investor_companies)
fig5 = px.pie(investor_companies, names='country', hole=0.5, color='country')
fig5.update_layout(title=dict(text='Fund by Country', x=0.5, y=0.9, xanchor='center', yanchor='top'), legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center', yanchor='top'))
col2.plotly_chart(fig5, use_container_width=True)

# Bubble map with animation
st.subheader("Bubble Map with Animation")
animated_data = data.groupby(['id_city', 'lat', 'lng', 'city', 'population', 'year']).agg({'value': 'sum'}).reset_index().sort_values('year')
fig6 = px.scatter_geo(animated_data, lat='lat', lon='lng', size='value', animation_frame='year', hover_name='city', hover_data=['id_city', 'population', 'value'], projection='orthographic')
st.plotly_chart(fig6)
