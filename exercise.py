import streamlit as st
import pandas as pd
import datetime

header = st.container()
dataset= st.container()
features = st.container()
model_trainig = st.container()

with header:
    st.title("Data Analysis of Unicorn Companies")
    st.text("In this application you will be able to analyze unicorn companies, comparing variables such as: countries, cities, type of industry, valuation.")

with dataset:
    st.title("Unicorns Companies Dataset")
    st.text("The daset used in this app is from kaggle:")
            
with features:
    st.title("Please, select the feaures")

with header:
    st.title("Data Analysis of Unicorn Companies")
    st.text("I")
