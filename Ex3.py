from __future__ import annotations
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from PIL import Image
import emoji
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px


from streamlit_plotly_events import plotly_events

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
        st.write("###### We have taken the information of unicorns companies from", unicornlink,"(1), ", GDPCountries, "(2) and ",bubbleCovid)




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
        industries=industries[variants!='non-who']
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
            indutry_filter = st.sidebar.multiselect('Industry', industries,industries)
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
            total_sum_industry = data[["Industry", "num_sequences"]]
            total_sum_industry.columns = ["Industry", "Total Companies"]

            graph = alt.Chart(total_sum_variant).mark_bar(
                opacity=0.7).properties(
                title='Total Cases by Variant').encode(
                x=alt.X('sum(Total Cases):Q',
                    title="Total Cases (log scale)",
                    scale=alt.Scale(type="log")),
                y=alt.Y('Variant:N',
                    title=None),
                color=alt.Color('Variant:N',
                    scale=alt.Scale(scheme='category20c')),
                tooltip = [alt.Tooltip('Variant:N'),alt.Tooltip('sum(Total Cases):Q')],
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
            cumsum_variant = data.groupby(["variant_grouped", "date"])["num_sequences"].sum().groupby(level=0).cumsum().reset_index()
            cumsum_variant.columns = ["Variant", "date", "Cumulative Cases"]

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



class Page3(Page):
    def __init__(self, data, **kwargs):
        name = "Page2"
        super().__init__(name, data, **kwargs)
    def content(self):
        st.write(emoji.emojize("""## :microbe: Dynamic World Map & GDP vs Infant Mortality Index :microbe:"""))

        st.write("""This section features the lates COVID-19 data from a global and economical perspective: the first visalisation will provide a
        overview of the evolution of Covid cases across the globe, while the second one will compare the GDP vs Infant Mortality index, an insightful index for the health status of a country, to the number of
        Covid cases in that country.""")

        # Importing first plot
        st.write("""#### World COVID-19 Cases - Evolution Over Time :earth_africa: """)

        #st.write("""##### The dataset used:""")
        df = pd.read_csv('cases_evolution.csv', index_col=0)
        #df
        st.write("###### Additional data for these insights was taken from", bubbleCovid, "and", GDPCovid )




        fig_1 = px.scatter_geo(
            df,
            locations='countryCode',
            color='continent',
            hover_name='country',
            projection='orthographic',
            size='cases',
            title=f'World COVID-19 Cases - Evolution Over Time',
            animation_frame="date"
        )

        st.plotly_chart(fig_1)


        st.write("""#### GDP :moneybag: vs Infant Mortality  :baby_bottle: & Total Cases""")

        #st.write("""##### The dataset used:""")
        ## Importing GDP vs Infant mortality dataframe
        data = pd.read_csv('data_gdp.csv', index_col=0)
        #data

        # Plot 2
        bubble_fig = px.scatter(data, x='Infant mortality (per 1000 births)',
                                        y='GDP ($ per capita)',
                                        color='Continent',
                                        size='Tot number of cases',
                                        log_x=True,
                                        hover_name="Country",
                                        hover_data=['GDP ($ per capita)', 'Infant mortality (per 1000 births)'],
                                        size_max=70)


        #bubble_fig.update_layout(hovermode='closest')
        st.plotly_chart(bubble_fig)
        # hovertemplaye=None
        # hovermode="x unified"

class Page4(Page):
    def __init__(self, data, **kwargs):
        name = "Page2"
        super().__init__(name, data, **kwargs)
    def content(self):
        data = pd.read_csv('data.csv')
        data=data.drop(["Unnamed: 0","Climate"], axis=1)
        def date_change(date_str):
                    format_str = '%Y-%m-%d' # The format
                    datetime_obj = datetime.strptime(date_str, format_str)
                    # print(datetime_obj.date())
                    return datetime_obj.date()

        data["date"] = data["date"].apply(date_change)

        variants=data['variant_grouped'].unique()
        variants=variants[variants!='non-who']
        locations=data['Country'].unique()
        chosen_variants = data.groupby('variant_grouped')['num_sequences'].sum().sort_values(ascending=False)[:5]


        #Create and name sidebar
        st.sidebar.header('Filter the Graphs')
        #st.sidebar.write("""#### Choose your SG bias""")
        variants=data['variant_grouped'].unique()
        variants=variants[variants!='non-who']
        locations=data['Country'].unique()
        country_list = sorted(set(data["Continent"]))
        country_list.insert(0,'All')
        sorted(country_list)

        def user_input_features():
                    time_filter = st.sidebar.slider('Time', 2020, 2021, 2020, 1)
                    variant_filter = st.sidebar.multiselect('Variant', variants,variants)
                    country_filter = st.sidebar.selectbox("Select a region:", country_list)
                    return time_filter, variant_filter,country_filter

        time_filter, variant_filter, country_filter = user_input_features()
        st.write(emoji.emojize("""# :microbe: COVID-19 Cases by month:"""))
        st.write("This interactive plot gives an overview of the monthly trends in covid evolution. "
        "The filters on the left give the option of choosing the year, region and variant we wish "
        "to study. On choosing any of the filters, both the plots will adjust accordingly. ")

        st.write("""### Click on any of the months on the first visualization to see the variant distribution """
        "of the total cases in that month. """)
        data['year']=pd.DatetimeIndex(data['date']).year
        data['month']=pd.DatetimeIndex(data['date']).month
        data['month']=pd.to_datetime(data['month'], format='%m').dt.month_name()
        #data

        #print(data)
        if st.sidebar.checkbox("Display all Data"):
            data1=data
            all_data_textbox = True
        else:
            all_data_textbox = False
            data=data[data.year==time_filter]
            if country_filter == 'All':
                data1=data[data.variant_grouped.isin(variant_filter)]
            else:
                data1 = data[data.Continent == country_filter]
                data1 = data1[data1.variant_grouped.isin(variant_filter)]
        #data1

        sum_month = data1.groupby(["month"])["num_sequences"].sum().reset_index()

        NEW=['January','February','March','April', 'May','June', 'July','August', 'September','October','November','December' ]

        r_cord=[]

        for i in NEW:
            if i not in np.array(sum_month['month']):
                r_cord.append(0)
            else:
                r_cord.append(int(sum_month[sum_month['month']==i].num_sequences))

        D=[]
        for i in range(len(r_cord)):
            D.append([NEW[i],r_cord[i]])

        Cases=pd.DataFrame(D, columns=["Month","Number of cases"])

        col1, col2 =st.columns(2)
        col1.metric("Year: ", time_filter)
        col2.metric("Region: ", country_filter)

        col1, col2 = st.columns(2)

        theta =np.linspace(90,450,13)
        theta=theta[0:12]
        selected_points={}
        with col1:
            fig = go.Figure()
            circle=np.linspace(0,360,60)
            circle_r=np.empty(len(circle))
            circle_r.fill(0.1)
            marker_size=r_cord/np.linalg.norm(r_cord)
            marker_size=marker_size*100
            fig.add_trace(go.Scatterpolar(
                    r = circle_r,
                    theta = circle,
                    mode = 'lines',
                    #hoverinfo='skip',
                    line_color = 'green',
                    #hoverinfo=None,
                    hoverinfo='skip',
                    showlegend = False
                ))
            a=str(np.sum(r_cord))

            fig.add_trace(go.Barpolar(
                r=r_cord,
                theta=theta,
                width=[1,1,1,1,1,1,1,1,1,1,1,1,],
                #marker_color=["#E4FF87", '#709BFF', '#709BFF', '#FFAA70', '#FFAA70', '#FFDF70', '#B6FFB4'],
                marker_line_color="green",
                text=['January','February','March','April', 'May','June', 'July','August', 'September','October','November','December' ],
                marker_line_width=1,
                opacity=0.8,
                #text=r_cord,
                #hoverinfo='text',
                hovertemplate ='Total no of cases<br>%{r:.2f}'

            )
            )
            fig.add_trace(go.Scatterpolar(
                r=[5,5,5,5,5,5,5,5,5,5,5,5],
                theta=theta,
                mode='markers + text',
                text=['January','February','March','April', 'May','June', 'July','August', 'September','October','November','December' ],
                fillcolor='green',
                marker_size=marker_size,
                customdata = [[NEW[i],r_cord[i]] for i in range(len(r_cord))],
                #name=r_cord,
                textposition="middle center",
                #hoverinfo='name',
                hovertemplate= '%{customdata[0]}<br>Total no of cases:<br>%{customdata[1]:.3f}'
            ))

            fig.add_trace(go.Scatterpolar(
                r=r_cord,
                theta=theta,
                mode='markers',
                fillcolor='green',
                marker_size=r_cord
            ))

            fig.update_layout(showlegend=False,
                template=None,
                polar = dict(
                    radialaxis = dict(range=[-4, 5], showline=False, showgrid=False,showticklabels=False, ticks=''),
                    angularaxis = dict(showline=False,showticklabels=False, showgrid=False, ticks='')
                )
            )

            selected_points = plotly_events(fig)

        month='All'
        if len(selected_points)!=0:
            month=selected_points[0]['pointNumber']
            month=NEW[month]
            data2=data1[data1['month']==month]
        else:
            data2=data1

        df  = data2.groupby(["variant_grouped"])["num_sequences"].sum().reset_index()
        df=df.rename(columns={"variant_grouped":"Variants", "num_sequences":"Total No. of cases"})
        df=df.sort_values(by=['Variants'],ascending=True)
        with col2:
            fig2= px.bar(df, x="Total No. of cases", y="Variants", orientation='h', color="Variants")
            fig2

        #st.write("The first plot represents total number of ")


        if month!='All':
            st.write("#### Month chosen: "+ month)

        st.write("The first visualization encodes the number of covid cases in each month through the marker size. "
        "For quantitative understanding, the values are given in the hover table as well. The second visualization "
        "is a representation of the covid cases during the time period (year/month if selected) by variants. ")
        st.write("Given below is also the data table for covid cases in each month." )
        Cases





def main():
    """A streamlit app template"""


    col_side_1, col_side_1, = st.columns((2,1))
    image = Image.open('covid_cell.jpeg')
    st.sidebar.image(image)
    st.sidebar.title("Navigation")
    PAGES = {
        "About the app": About,
        "Covid by Variants": Page2,
        "Covid in a Geographical Context": Page3,
        "Overall Development": Page4,

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
