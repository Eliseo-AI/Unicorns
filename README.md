# Unicorns
The term “unicorn” was first coined in 2013 by Aileen Lee, the founder of Cowboy Ventures, a US-based seed-stage venture capital firm. In a TechCrunch article Welcome to The Unicorn Club: Learning from Billion-Dollar Startups (2013), she named a startup company valued at US $1 Billion or more as a unicorn. [Article-Jan,2023](https://www.alphajwc.com/en/the-differences-between-unicorn-decacorn-and-hectocorn/)
Table of Content
================
* [Interactive-Unicorns_Companies-Dashboard](#Interactive-Unicorns_Companies-Dashboard)
  * [Description](#description)
  * [Datasets](#datasets)
  * [Installation Requirements](#installation-requirements)
  * [Licensing](#licensing)
  * [Authors](#Authors)

# Interactive-Unicorns-Dashboard
[Streamlit app](https://eli-2020-unicorns-streamlit-1oh7v8.streamlitapp.com/)

## Description
A work of building an interactive dashboard to provide insights about Unicorns Companies globally by master's student from the [Digital Sciences Track of Université Paris Cité](https://u-paris.fr/en/master-aire-digital-sciences/). 

## Datasets


Columns in the datasets:

- `unicorns`: the name of the company
- `country / region`: identifies the name of the country
- `Province / state`: identifies the name of the states
- `Lat`: the geographic coordinates that specifies the north – south position of a point on the Earth's surface.
- `Lng`: the geographic coordinates that specifies the east – west position of a point on the Earth's surface.
- `Date`: identifies the cumulative cases per day in each of the countries.

To calulcate the normalization we acquire to get the population of the each country https://www.kaggle.com/tanuprabhu/population-by-country-2020 and we only used `Country and Population`. 


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
