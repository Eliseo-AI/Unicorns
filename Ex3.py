from __future__ import annotations
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime

unicornlink = '[Github](https://github.com/Eli-2020/Unicorns)'
companies='[Kaggle](https://www.kaggle.com/datasets/yamqwe/omicron-covid19-variant-daily-cases?select=covid-variants.csv)'
GDPCountries = '[Kaggle](https://www.kaggle.com/code/thejeswar/gdp-population-analysis-of-the-world-countries/notebook)'

st.set_page_config(
    page_title="A Dashboard Template",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache()
def fake_data():
    """some fake data"""

    dt = pd.date_range("2021-01-01", "2021-03-01")
    df = pd.DataFrame(
        {"datetime": dt, "values": np.random.randint(0, 10, size=len(dt))}
    )

    return df


def sidebar_caption():
    """This is a demo of some shared sidebar elements.
    Reused this function to make sure we have the same sidebar elements if needed.
    """

    #st.sidebar.header("Yay, this is a sidebar")
    #st.sidebar.markdown("This is a markdown element in the **sidebar**.")


def filter_table_option():

    show_n_records = st.sidebar.slider('Show how many', 0, 30, 1)

    return show_n_records


class Page:
    def __init__(self, name, data, **kwargs):
        self.name = name
        self.data = data
        self.kwargs = kwargs

    def content(self):
        """Returns the content of the page"""

        raise NotImplementedError("Please implement this method.")

    def title(self):
        """Returns the title of the page"""
        st.header(f"{self.name}")

    def __call__(self):
        #self.title()
        self.content()



class About(Page):
    def __init__(self, data, **kwargs):
        name = "About"
        super().__init__(name, data, **kwargs)


    def content(self):

       
        st.write("""## How it works""")
        st.write("This tool will enable users to quickly visualize Companies in global economy, "
        "track the development of the unicorns companies and its industries and measure the correlation "
        "between the development of a country and the number of Companies.")
        st.write("##### For viewing the Sourcecode, click here:", unicornlink)
        st.write("""## Navigating the app""")
        st.write("The app consists of 3 pages, including this introduction page. "
        " To navigate to the other pages, click on the options in the sidebar. "
        "Given below is a short description of what each page shows.")
        st.write("##### 1: Companies by Industry")
        st.write("The first page is a view of the companies by industry. We can "
        "compare companies creation in different locations at different times around the "
        "world")
        st.write("##### 2: How Companies have been created")
        st.write("In the second page, we go deeper into understanding the creation of companies. "
        "We see the evolution of companies over time and also, make a comparison of regions by GDP per capita"
        "and creation of Unicorns companies if there is some trend that is observable. ")
        st.write("##### 3: Monthly creation evolution")
        st.write("Here, we have a monthly view of how companies have been createdd by location "
        "and industries ")
        st.write("###### We have taken the information of unicorns companies from", unicornlink,"(1), ", GDPCountries, "(2) ")




class Page2(Page):
    def __init__(self, data, **kwargs):
        name = "Page2"
        super().__init__(name, data, **kwargs)
    def content(self):
        #Create header
        #st.write("""## How it works""")
        st.write("This tool will enable users to quickly visualize Companies global evolution, "
        "track the development of the Unicorns and its industries and measure the correlation "
        "between the development of a country and the number of Unicorns Companies.")
        #st.write("##### For viewing the Sourcecode, click here:", linkedinlink)


        #Bring in the data
        data = pd.read_csv('new_uni.csv')
        #st.write("## THE DATA BEING USED")
        data=data.drop(["Unnamed: 0","Valuation"], axis=1)

        #Transformation of Date column
        def date_change(date_str):
            format_str = '%Y-%m-%d' # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            # print(datetime_obj.date())
            return datetime_obj.date()

        data["Date"] = data["Date"].apply(date_change)

        industries=data['Industry'].unique()
        industries=industries[industries!='non-who']
        locations=data['Country'].unique()
        
        #Create and name sidebar
        st.sidebar.header('Filter the Graphs')
        #st.sidebar.write("""#### Choose your SG bias""")
        industries=data['Industry'].unique()
        industries=industries[industries!='non-who']
        
        country_list = sorted(set(data["Country"]))
        country_list.insert(0,'All')
        sorted(country_list)

        def user_input_features():
            time_1,time_2 = st.sidebar.date_input("Choose a Range in Time:", value = (data.date.min(),data.date.max()), min_value =data.date.min(), max_value=data.date.max())
            country_filter = st.sidebar.selectbox("Select a Country:", country_list)
            return time_1, time_2, variant_filter,country_filter

        time_1, time_2, variant_filter, country_filter = user_input_features()

        if st.sidebar.checkbox("Display all Data"):
            data1=data
            all_data_textbox = True
        else:
            all_data_textbox = False
            if country_filter == 'All':
                data1=data[(data.variant_grouped.isin(variant_filter)) & (time_1<=data.date) & (time_2>=data.date)]
            else:
                data1 = data[data.Continent == country_filter]
                data1 = data1[(data1.variant_grouped.isin(variant_filter)) & (time_1<=data1.date) & (time_2>=data1.date)]
        data1


        st.write("## Chosen Filters: ")
        if all_data_textbox == True:
            st.write("All Data is chosen")
        else:
            st.write("Timeframe: " +str(time_1) + " to " + str(time_2))
            str_val = ", ".join(variant_filter)
            st.write("Chosen Industry: " + str(str_val))
            st.write("Chosen Country: " + str(country_filter))


        #Output rankings based on users selections
        st.write(
            """
            ## Overview of the Variants :chart_with_upwards_trend:
            """
        )

        def block1(data):

          def total_cases(data, click):
            '''
            Expects data.csv or its subsets as input
            Returns the horizontal bar chart showing the total cases by variant
            '''

            #Data manipulation: simple sum of cases by variant
            total_sum_industry = data[["Industry", "Value"]]
            total_sum_industry.columns = ["Industry", "Value"]

            graph = alt.Chart(total_sum_industry).mark_bar(
                opacity=0.7).properties(
                title='Total Cases by Industry').encode(
                x=alt.X('sum(Total Cases):Q',
                    title="Total Cases (log scale)",
                    scale=alt.Scale(type="log")),
                y=alt.Y('Industry:N',
                    title=None),
                color=alt.Color('Industry:N',
                    scale=alt.Scale(scheme='category20c')),
                tooltip = [alt.Tooltip('Industry:N'),alt.Tooltip('sum(Total Cases):Q')],
                opacity = alt.condition(click, alt.value(0.9), alt.value(0.1))).add_selection(
                click
            )

            return graph

          def cum_cases(data, click):
            '''
            Expects data.csv or its subsets as input
            Returns the graph showing cumulative cases by variant over time
            '''

            # Data manipulation: cumulative counts of cases by date and variant
            cumsum_variant = data.groupby(["Industry", "Date"])["Value"].sum().groupby(level=0).cumsum().reset_index()
            cumsum_variant.columns = ["Industry", "Date", "Value"]

            # Define interaction (needs to be global variable for cross-chart interaction)
            # click = alt.selection_single(encodings=['color'], on="mouseover")

            # Create plot
            graph = alt.Chart(cumsum_variant).mark_area(
                opacity=0.7,
                interpolate='basis',
                line=True).properties(
                title='Cumulative Cases by Variant over time').encode(
                x=alt.X("date:T",
                    title="Time Horizon",),
                y=alt.Y("Cumulative Cases:Q"),
                color=alt.Color('Variant:N',
                    scale=alt.Scale(scheme='category20c')),
                tooltip = [alt.Tooltip('Variant:N'),alt.Tooltip('Cumulative Cases:Q')],
                opacity = alt.condition(click, alt.value(0.9), alt.value(0.1))).add_selection(
                click
            )

            return graph

          def waves(data, click):
            '''
            Expects data.csv or its subsets as input
            Returns the graph showing cumulative cases by variant over time
            '''

            # Data manipulation: cumulative counts of cases by date and variant
            sum_variant = data.groupby(["variant_grouped", "date"])["num_sequences"].sum().reset_index()
            sum_variant.columns = ["Variant", "date", "Cases"]

            # Define interaction (needs to be global variable for cross-chart interaction)
            # click = alt.selection_single(encodings=['color'], on="mouseover")

            # Create plot
            graph = alt.Chart(sum_variant).mark_area(
              opacity=0.7,
              interpolate='basis',
              line=True).properties(
              title='Cases by Variant over time').encode(
              x=alt.X("date:T", title="Time Horizon",),
              y=alt.Y("Cases:Q", stack=None),
              color=alt.Color('Variant:N', scale=alt.Scale(scheme='category20c')),
              tooltip = [alt.Tooltip('Variant:N'),alt.Tooltip('Cases:Q')],
              opacity = alt.condition(click, alt.value(0.9), alt.value(0.1))).add_selection(
              click
            )

            return graph

          def cases_countries(data, click):
            '''
            Expects data.csv or its subsets as input
            Returns the graph showing cumulative cases by variant over time
            '''

            # Data manipulation: cumulative counts of cases by date and variant
            variantsum = data.groupby(["variant_grouped", "Country"])["num_sequences"].sum().reset_index()
            variantsum.columns = ["Variant", "Country", "Total Cases"]

            # Define interaction
            #click = alt.selection_single(encodings=['color'], on="mouseover")
            # Create plot

            graph = alt.Chart(variantsum).mark_bar(
              opacity=0.7,
              interpolate='basis',
              line=True).properties(
              title='Cases by Variant').encode(
              x=alt.X('Total Cases:Q', stack = 'normalize'),
              y=alt.Y("Country:N", title=None),
              color=alt.Color('Variant:N', scale=alt.Scale(scheme='category20c'),legend=alt.Legend(title="Variants")),
              tooltip = [alt.Tooltip('Country:N'), alt.Tooltip('Variant:N'), alt.Tooltip('Total Cases:Q')],
              opacity = alt.condition(click, alt.value(0.9), alt.value(0.1))
            ).add_selection(
              click
            )#.properties(width=600)

            return graph

          click = alt.selection_single(encodings=['color'], on="mouseover", resolve="global")

          return (total_cases(data,click) & (waves(data, click) & cum_cases(data, click)) | cases_countries(data, click))

        st.altair_chart(block1(data1))


        #################

        # Disable default datapoints limit in Altair
        alt.data_transformers.disable_max_rows()



    def main():
        """A streamlit app template"""


        col_side_1, col_side_1, = st.columns((2,1))
        st.sidebar.title("Navigation")
        PAGES = {
            "About the app": About,
            "Covid by Variants": Page2,
            

        }

        # Select pages
        # Use dropdown if you prefer
        selection = st.sidebar.radio("Pages", list(PAGES.keys()))
        sidebar_caption()

        page = PAGES[selection]

        DATA = {"base": fake_data()}

        with st.spinner(f"Loading Page {selection} ..."):
            page = page(DATA)
            page()


    if __name__ == "__main__":
        main()