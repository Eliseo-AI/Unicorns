# Unicorns
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
The data sets are from the open data of [Jonhs Hopkins University](https://github.com/CSSEGISandData/COVID-19)
* Dataset_COVID_Death_complete.csv
* Dataset_COVID_confiremed_complete.csv
* Dataset_COVID_recovered_complete.csv

Columns in the datasets:

- `Country / region`: identifies the name of the country
- `Province / state`: identifies the name of the states
- `Latitude`: the geographic coordinates that specifies the north – south position of a point on the Earth's surface.
- `Longitude`: the geographic coordinates that specifies the east – west position of a point on the Earth's surface.
- `Date`: identifies the cumulative cases per day in each of the countries.

To calulcate the normalization we acquire to get the population of the each country https://www.kaggle.com/tanuprabhu/population-by-country-2020 and we only used `Country and Population`. 


## Installation Requirements

- Install the project dependencies run pip install -r requirements.txt
```
pip install -r requirements.txt
```
- Requirements includes:
```
pandas == 1.4.3
streamlit==1.11.0
plotly.express==0.4.0
numpy==1.23.1
```
To run the streamlit code
```
streamlit run app.py
```
## Licensing
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Authors:

* **Eliseo Baquero** [@Eli-2020](https://github.com/Eli-2020)
