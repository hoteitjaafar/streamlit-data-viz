import pandas as pd 
import streamlit as st 
from datetime import datetime, timedelta 
from matplotlib import pyplot as plt 
from matplotlib import dates as mpl_dates 

plt.style.use('fivethirtyeight')

new_data = 'globalsalesdata.csv'

@st.cache 
def load_data():
    data = pd.read_csv(new_data)
    return data

df = load_data()

df = df.head(5000)

st.title('Analyzing Global Sales Data')
st.write('')
st.write('')
if st.checkbox('Display/Hide Instructions'):
    st.write('''You will first have to access the side bar. This application
                will allow you to analyze a number of markets by Sub-Category, Category, 
    and Segment.''')
    st.write('''Furthermore, this application will allow you to identify
                the highest and lowest sources of sales by state, for each country. ''')




if st.sidebar.checkbox('Analyze Market'):
    unique_market = df['Market'].unique()
    market = st.sidebar.selectbox('Select Market', unique_market)
    filt = df['Market'] == market 

    analysis = ['Sub-Category', 'Category', 'Segment']
    analysis_select = st.sidebar.selectbox('What do you want to analyze?', analysis)

    new_one = df.loc[filt, ['Sales', analysis_select]]
    new_one.sort_values(by='Sales', ascending=False, inplace=True)

    chosen_analysis = new_one[analysis_select]
    sales = new_one['Sales']

    if st.checkbox('Display/Hide Market Analysis'):
        fig, ax = plt.subplots()
        ax.barh(chosen_analysis, sales, color='steelblue')
        ax.set_title('Market Analysis: {} Sales by {}'.format(market, analysis_select))
        ax.set_xlabel('Total Sales')
        ax.set_ylabel('{}'.format(analysis_select))
        plt.tight_layout()
        st.pyplot(fig)

st.sidebar.markdown('#')


if st.sidebar.checkbox('Total Sales by State'):
    unique_country = df['Country'].unique()
    country = st.sidebar.selectbox('Select Country', unique_country)
    filt2 = df['Country'] == country 
    country_df = df.loc[filt2]


    status = st.sidebar.radio('Display Top or Bottom 10 Records?', ['Top', 'Bottom'])

    if status == 'Top':
        country_df.sort_values(by='Sales', ascending=False, inplace=True)
        country_df = country_df.nlargest(10, 'Sales')    
        state = country_df['State']
        sales2 = country_df['Sales']

        if st.checkbox('Display/Hide Top Sales by State'):
            fig2, ax2 = plt.subplots()
            ax2.barh(state, sales2, color='steelblue')
            ax2.set_title('Top Sales by State')
            ax2.set_xlabel('Total Sales')
            ax2.set_ylabel('States')
            plt.tight_layout()
            st.pyplot(fig2)
    
    if status == 'Bottom':
        country_df.sort_values(by='Sales', ascending=False, inplace=True)
        country_df = country_df.nsmallest(10, 'Sales')
        state = country_df['State']
        sales2 = country_df['Sales']

        if st.checkbox('Display/Hide Bottom Sales by State'):
            fig2, ax2 = plt.subplots()
            ax2.barh(state, sales2, color='steelblue')
            ax2.set_title('Bottom Sales by State')
            ax2.set_xlabel('Total Sales')
            ax2.set_ylabel('States')
            plt.tight_layout()
            st.pyplot(fig2)




