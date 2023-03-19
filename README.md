Table of Content
================
* [Interactive-Unicorns_Companies-Dashboard](#Interactive-Unicorns_Companies-Dashboard)
  * [Definition](#definition)
  * [Description](#description)
  * [Datasets](#datasets)
  * [Installation Requirements](#installation-requirements)
  * [Licensing](#licensing)
  * [Authors](#Authors)

# Interactive-Unicorns-Dashboard
- Scatter Plot GRaph by Country (Comparison by years 2011-2022)
- Bubble Graph by Industry (Acumulate Value by Industry)
- Box Plot Graph (Comparison)
- Map Visualization of Unicorn Companies
- Investor Analysis (Funds, Countries)
- Buble Map with Animation (During Years, by Cities)
See all the graphs in the link [Streamlit app](https://eli-2020-unicorns-streamlit-1oh7v8.streamlitapp.com/)
## Definition
The term “unicorn” was first coined in 2013 by Aileen Lee, the founder of Cowboy Ventures, a US-based seed-stage venture capital firm. In a TechCrunch article Welcome to The Unicorn Club: Learning from Billion-Dollar Startups (2013), she named a startup company valued at US $1 Billion or more as a unicorn. [Article-Jan,2023](https://www.alphajwc.com/en/the-differences-between-unicorn-decacorn-and-hectocorn/)
## Description
A work of building an interactive dashboard to provide insights about Unicorn Companies globally by master's student from the [Digital Sciences Track of Université Paris Cité](https://u-paris.fr/en/master-aire-digital-sciences/). 

## Datasets


Columns in the datasets:

- unicorns: the name of the company
- ranking_companies = ranking of companies by market value
- date_joined = official start of each company
- country = country
- city = city 
- industry = industry category 
- selected_investros = funds that invested in the company 
- value = company value in trillions of dollars 
- lat = latitude
- lng = longitude 
- capital = city type category ("primary" = country capital, "admin" = regional capital, "minor"= metropolitan city, "" = city) 
- population= population of the city. 
- id_city = international identification number of the city.

## Installation Requirements

- Install the project dependencies run pip install -r requirements.txt
```
pip install -r requirements.txt
```
- Requirements includes:
```
pandas == 1.5.3
streamlit==1.19.0
plotly.express==0.4.0
altair==4.2.2 
numpy==1.23.1
pydeck==0.7.1
folium==0.14.0
```
To run the streamlit code
```
streamlit run exercise.py
```
## Licensing
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Authors:

* **Eliseo Baquero** [@Eli-2020](https://github.com/Eli-2020)
