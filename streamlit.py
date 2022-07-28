import streamlit as st
import pandas as pd
import numpy as np
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
    st.text('The dateset include the total of Unicorns companies around the world top 5 Unicorns by Valuation in US$')
   
    data_unicorn = pd.read_csv('data/unicorns_2022.csv', sep=',')
    st.write(data_unicorn.head())
    
    st.subheader('Total Valuation of Unicorns by Country')
    countries = pd.DataFrame(data_unicorn.groupby(["country"])["value"].sum()).head(50)
    st.bar_chart(countries)
    
    st.subheader('Total Valuation by Industry')
    industry_value = pd.DataFrame(data_unicorn.groupby(["industry"])["value"].sum()).head(50)
    st.bar_chart(data=industry_value)
        
    st.subheader('Choose the Best combination between date and age range for you')
    
    data_unicorn['date_joined'] = pd.to_datetime(data_unicorn['date_joined']).dt.strftime('%Y-%m-%d')
    
    industry_options = data_unicorn['industry'].unique().tolist()
    date_options = data_unicorn['date_joined'].unique().tolist()
    
    date = st.selectbox("Which date would you like to see", date_options,100)
    industry_u = st.multiselect("Which industry would you like to see", industry_options, ['Fintech'])
    
    data_unicorn = data_unicorn[data_unicorn['industry'].isin(industry_u)]
    data_unicorn = data_unicorn[data_unicorn['date_joined']==date]
    
    fig2 = px.bar(data_unicorn,x="industry",y="value",color="industry", range_y=[0,500])
    
    fig2.update_layout(width=800)
    
    st.write(fig2)
    
    
