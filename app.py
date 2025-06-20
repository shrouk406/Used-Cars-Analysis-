
import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import io

st.set_page_config(layout = 'wide', page_title = 'Used Cars EDA')

url = "https://drive.google.com/uc?export=download&id=1CEhGMmpIb0ESL9cK_RS4Q3fhXTKVjpBF"

response = requests.get(url)
if response.status_code == 200:
    df = pd.read_csv(io.BytesIO(response.content))
    print("✅ File loaded successfully!")
    print(df.head())
else:
    print(f"❌ Error downloading file: {response.status_code}")

page = st.sidebar.selectbox('GO To:', ['Data Overview', 'Univariate Analysis', 'Bivariate Analysis', 'Multivariate'])


if page == 'Data Overview':
    st.write('# Welcome To the Analysis of the Used Cars Dataset!')
    
    st.image('https://themanufacturer-cdn-1.s3.eu-west-2.amazonaws.com/wp-content/uploads/2018/02/14122735/With-enough-effort-a-used-car-can-be-almost-new-again.-Image-Public-Domain.-1024x713.jpg')

    st.markdown("""
    ###  Dataset Overview

    This dataset contains detailed listings of used cars posted for sale. It includes information such as vehicle year, price, mileage (odometer), fuel type, transmission, drive type, condition, and more. The data has been preprocessed to include both numerical and categorical variables, enabling meaningful analysis and visualizations. It is ideal for exploring trends in car pricing, understanding feature relationships, and building machine learning models for price prediction.
    """)

    st.dataframe(df.head())

    st.write("Data Summary for numeric values:")
    st.write(df.describe(include = 'number').round(4))


    st.write("Data Summary for categorical values:")
    st.write(df.describe(include = 'object'))


    st.write("Top 5 Most Expensive Cars:")
    st.dataframe(df.sort_values(by='price', ascending=False).head(5))


elif page == 'Univariate Analysis':
    col = st.selectbox('Select Column', df.columns)
    
    chart = st.selectbox('Select Chart', ['Histogram', 'Box', 'Pie'])

    if chart == 'Histogram':
        st.plotly_chart(px.histogram(df, x = col, title= col))

    elif chart == 'Box':
        st.plotly_chart(px.box(data_frame= df, x= col, title= col))

    elif chart == 'Pie':
        st.plotly_chart(px.pie(data_frame= df, names= col, title= col))


    st.write('# Some Analysis Questions to check!')
    
    st.header('Q1: What is the distribution of car prices?')  
    st.plotly_chart(px.histogram(data_frame= df, x = 'price'))
    st.write("depending on the chart: the prices vary from to almost 50k ")

    st.header('Q2: What are the most common car manufacturing years')  
    st.plotly_chart(px.histogram(data_frame= df, x = 'year'))
    st.write("depending on the chart: the most common car manufacturing years 2013 - 2018")

    st.header('Q3: What is the most frequent fuel type?')  
    st.plotly_chart(px.pie(df, names = 'fuel'))
    st.write("depending on the chart: the most frequent fuel type is Gas")

    st.header('Q4: What are the most common car conditions listed?')  
    st.plotly_chart(px.pie(df, names= 'condition', labels= {'condition': 'Car Condition'}))
    st.write("depending on the chart: the most common car conditions age good then excellent")

    st.header('Q5: What is the distribution of odometer readings (mileage)?')  
    st.plotly_chart(px.histogram(df, x= 'odometer', width= 900, height= 400))
    st.write("depending on the chart: the odometers vary from 0 to 500k")
    st.write("The most are from 60k to almost 200k")

    st.header('Q6: Which transmission type appears most frequently?')  
    st.plotly_chart(px.pie(df, names= 'transmission', labels= {'transmission': 'Transmission Type'}))
    st.write("depending on the chart: the most frequent transmission is automatic")

    st.header('Q7: What are the most common vehicle sizes ?')  
    st.plotly_chart(px.pie(df, names= 'size', labels= {'size': 'Vehicle Size'}))
    st.write("depending on the chart: the most common vehicle size is the full size")

elif page == 'Bivariate Analysis':


    col_1 = st.selectbox('Select the first Column', df.columns)
    col_2 = st.selectbox('Select the second Column', df.columns)

    chart = st.selectbox('Select Chart', ['Scatter', 'Box', 'Bar'])

    if chart == 'Scatter':
        st.plotly_chart(px.scatter(df, x = col_1, y = col_2))

    elif chart == 'Box':
        st.plotly_chart(px.box(df, x = col_1, y = col_2))

    elif chart == 'Bar':
        st.plotly_chart(px.bar(df, x = col_1, y = col_2))    


    st.write('# Some Analysis Questions to check!')


    st.header('Q1: Does the year of the car affect its price?')  
    st.plotly_chart(px.scatter(df, x= 'year', y= 'price', width= 900, height= 400))
    st.write('depending on the chart: the year isn\'t affecting the price')
#

    st.header('Q2:  What is the relationship between car condition and price?')  
    st.plotly_chart(px.box(df, x= 'condition', y= 'price', width= 900, height= 400))
    sns.barplot(df, x= 'condition', y= 'price')
    st.write('depending on the charts: when the condition is [New or Good], the price is higher')

 

    st.header('Q3: How does odometer reading affect price?')  
    st.plotly_chart(px.scatter(df, x= 'odometer', y= 'price', width= 900, height= 400))
    st.write('depending on the chart: If The odometer reading is high, the car price is low, Makes sense!')


    st.header('Q4: Does drive type (e.g., FWD, RWD, 4WD) influence price?')  
    st.plotly_chart(px.box(df, x= 'drive', y= 'price', width= 900, height= 400))
    st.write('depending on the chart: The 4WD drivers has the highest prices')


    st.header('Q5: Is there a price difference based on fuel type (gas, electric, hybrid)?')  
    st.plotly_chart(px.box(df, x= 'fuel', y= 'price', width= 900, height= 400))
    st.write('depending on the chart: YES!, Diesel and Electric have the higher prices than others')


elif page == 'Multivariate':
    
    st.header('Q1: Show The correlation between all columns with the car price')  
    correlation = df.corr(numeric_only= True)
    fig, ax = plt.subplots()
    sns.heatmap(correlation, ax=ax)
    st.pyplot(fig)
