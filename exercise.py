import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

header = st.beta_container()
dataset= st.beta_container()
features = st.beta_container()
model_trainig = st.beta_container()

with header:
    st.title("Data Analysis of Unicorn Companies")
    st.text("In this application you will be able to analyze unicorn companies, comparing variables such as: countries, cities, type of industry, valuation.")

with dataset:
    st.title("Unicorns Companies Dataset")
    st.text("The daset used in this app is from kaggle:
            
with features:
    st.title("PLease, select the feaures")

with header:
    st.title("Data Analysis of Unicorn Companies")
    st.text("I")