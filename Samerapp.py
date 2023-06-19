


#Import Libraries 

import pandas as pd
import streamlit as st
import hydralit_components as hc
import requests
from streamlit_lottie import st_lottie
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px  
import streamlit_card as st_card
import numpy as np
from pathlib import Path
import base64


########################################################################################################################################################
########################################################################################################################################################

#Impporting Data

df = pd.read_csv('Dementia data for MSBA 350E (1).csv')



########################################################################################################################################################
########################################################################################################################################################

# Creating Navigation Bar for streamlit app
#make it look nice from the start
st.set_page_config(layout='wide' ,page_title= 'Dementia Lebanon',
page_icon= '🧠', initial_sidebar_state= 'expanded')

def display_app_header(main_txt,sub_txt,is_sidebar = False):
    """
    function to display major headers at user interface
    ----------
    main_txt: str -> the major text to be displayed
    sub_txt: str -> the minor text to be displayed 
    is_sidebar: bool -> check if its side panel or major panel
    """

    html_temp = f"""
    <h2 style = "color:#010101; text_align:center;"> {main_txt} </h2>
    <p style = "color:#010101; text_align:center;"> {sub_txt} </p>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(html_temp, unsafe_allow_html = True)
    else: 
        st.markdown(html_temp, unsafe_allow_html = True)


# specify the primary menu definition
menu_data = [
    {'icon': "💟", 'label':"Patients & Caregivers ",'ttip':"discover"},
    {'icon': "🗣️", 'label':"Symptoms"},
]

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded



over_theme = {'menu_background':'#6B6D71'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Overview and Data', #will show the st hamburger as well as the navbar now!
    sticky_nav=False, #at the top or not
    hide_streamlit_markers=False,
    sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
)


def load_lottieurl(url):
    r= requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie= load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_iqbweiiz.json')
#lottie2 = load_lottieurl('')


########################################################################################################################################################################





if menu_id== 'Overview and Data':
    st.markdown("<h1 style='text-align: center;'>Dementia Conditions in Lebanon</h1>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: left;'>Overview of Dementia</h2>", unsafe_allow_html=True)

    left,right = st.columns((2,1))

    with left:
        st.markdown("")
        # Write a brief about Dementia
        display_app_header(main_txt='What is Demenetia?',
                    sub_txt= "Dementia is a general term that encompasses a range of conditions causing impaired memory, thinking, and decision-making, hindering daily activities. Alzheimer's disease is the most prevalent type, accounting for 60-80 percent of cases. Dementia is not a specific disease but a syndrome with various possible causes. Symptoms can vary depending on the underlying condition and its stage. Early signs include forgetfulness, word-finding difficulties, confusion, and mood or behavior changes. As dementia progresses, memory, language, judgment, and motor skills may deteriorate. Treatment involves symptom management, addressing underlying conditions, and providing support to individuals and caregivers. Non-drug interventions like cognitive stimulation therapy, occupational therapy, and social support programs can be helpful. Creating a safe environment with modifications, routines, and supervision is crucial. Caregiver support and education play a vital role in managing the challenges of dementia caregiving.\n\n"
                )
    
    with right:
        st_lottie(lottie, height= 350,key= 'coding') 


    display_app_header(main_txt='What are the Symptoms?',
                    sub_txt= "• The team identifies more than 50 symptoms, but for simplicuty reasons I removed plenty and kept on 25 symptoms.\n\n"
                    "• Some people experience no/or minor symptoms.\n\n"
                    "• I divided the symptoms in this application into three categories: physical, psychological & emotional, and mental & cognitive symptoms.\n\n"
                )  

    display_app_header(main_txt='Data Collection',
            sub_txt= 
            "• Epidemiology and Population Health Department at FHS-AUB initaited a study to identify the Denmentia cases across Lebanon and compare it to regional and global figures.\n\n"
            "• The study revealed a crude dementia prevalence of 7.4 percent among the studied population.\n\n"
                ) 
    st.subheader('Data Sample:')
    # Filter data based on location
    location = st.selectbox('Select Location', df['Location'].unique())
    filtered_df = df[df['Location'] == location]

    # Display the filtered DataFrame sample
    st.write(f"Sample data for Location, first 5 rows: {location}")
    st.dataframe(filtered_df.sample(n=5))


if menu_id== 'Patients & Caregivers ':

    st.markdown("<h1 style='text-align: center;'>Analysis of Patients and Caregivers Data</h1>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")

    st.markdown("<h3 style='text-align: left;'>Patients and Caregivers Analysis based on Location</h3>", unsafe_allow_html=True)

    col11,col22 = st.columns ((1,1))

    with col11: 

        # Actual count or frequency of each location
        count_beirut = 311
        count_aley = 72
        count_chouf = 102

        # Calculate the total count
        total_count = count_beirut + count_aley + count_chouf

        # Calculate the percentages
        percent_beirut = (count_beirut / total_count) * 100
        percent_aley = (count_aley / total_count) * 100
        percent_chouf = (count_chouf / total_count) * 100

        # Data for the pie chart
        percentages = [percent_beirut, percent_aley, percent_chouf]
        labels = ['Beirut', 'Aley', 'Chouf']
        colors = ['#4F94CD', '#00C957', '#808080']

        # Create the pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=percentages, hole=0.3, 
                            marker=dict(colors=colors))])
        fig.update_layout(title='Location Distribution')

        # Render the chart using Streamlit
        st.plotly_chart(fig,use_container_width=True)

    with col22:

        # Data for the stacked bar chart
        data = {
        'Location': ['Beirut', 'Aley', 'Chouf'],
        'Yes': [305, 30, 74],
        'No': [6, 42, 28]
}

        df = pd.DataFrame(data)

        # Calculate the total responses
        total_responses = 485

        # Calculate the percentage for each category
        df['Yes(%)'] = (df['Yes'] / total_responses) * 100
        df['No(%)'] = (df['No'] / total_responses) * 100

        # Set the index to 'Location' column
        df.set_index('Location', inplace=True)

        # Define the colors
        colors = ['#1f4462', '#8c8c8c']

        # Create the stacked bar chart using Plotly
        fig1 = go.Figure(data=[
        go.Bar(name='Yes', x=df.index, y=df['Yes(%)'], marker_color=colors[0]),
        go.Bar(name='No', x=df.index, y=df['No(%)'], marker_color=colors[1])
])

        # Set the chart title and labels
        fig1.update_layout(
            title='Income Distribution by Location',
            xaxis_title='Location',
            yaxis_title='Percentage (%)'
)

        # Render the chart using Streamlit
        st.plotly_chart(fig1,use_container_width=True)


    # Create a DataFrame with the data
    data = {
        'Location': ['Aley', 'Chouf', 'Beirut'],
        'Yes': [30, 74, 305],
        'No': [42, 28, 6]
}
    df = pd.DataFrame(data)

    # Set the Location column as the index
    df.set_index('Location', inplace=True)

    # Calculate the percentages
    df['Total'] = df['Yes'] + df['No']
    df['Yes %'] = (df['Yes'] / df['Total']) * 100
    df['No %'] = (df['No'] / df['Total']) * 100

    # Round the percentages to two decimal places
    df['Yes %'] = df['Yes %'].round(2)
    df['No %'] = df['No %'].round(2)

    # Define the colors
    colors = ['#1f4462', '#8c8c8c']

    # Create the stacked bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Yes', x=df.index, y=df['Yes %'], text=df['Yes %'], textposition='auto', marker_color=colors[0]),
        go.Bar(name='No', x=df.index, y=df['No %'], text=df['No %'], textposition='auto', marker_color=colors[1])
])

    # Set the chart title and labels
    fig.update_layout(
        xaxis_title='Location',
        yaxis_title='Percentage (%)'
)


    # Set the title of the web app
    st.markdown("<h5 style='text-align: left;'>Relationship Between Location and Caregiver Relation to Patient</h5>", unsafe_allow_html=True)

    # Add a select box to choose the location(s)
    selected_locations = st.multiselect('Select Location(s)', df.index.tolist(), default=df.index.tolist())

    # Filter the DataFrame based on the selected locations
    filtered_df = df.loc[selected_locations]

    # Create the filtered stacked bar chart
    filtered_fig = go.Figure(data=[
        go.Bar(name='Yes', x=filtered_df.index, y=filtered_df['Yes %'], text=filtered_df['Yes %'], textposition='auto', marker_color=colors[0]),
        go.Bar(name='No', x=filtered_df.index, y=filtered_df['No %'], text=filtered_df['No %'], textposition='auto', marker_color=colors[1])
    ])

    # Set the chart title and labels
    filtered_fig.update_layout(
        xaxis_title='Location',
        yaxis_title='Percentage (%)'
    )

    # Display the filtered chart
    st.plotly_chart(filtered_fig,use_container_width=True)

    # Create a DataFrame with the data
    data = {
        'Location': ['Beirut', 'Aley', 'Chouf', 'Beirut', 'Aley', 'Chouf'],
        'Caregiver relation to patient': [
        'son/daughter', 'husband/wife', 'husband/wife', 'husband/wife', 'husband/wife', 'husband/wife'
    ]
}
    df = pd.DataFrame(data)

    # Calculate the percentage for each combination of location and caregiver relation
    percentage_df = df.groupby(['Location', 'Caregiver relation to patient']).size().reset_index(name='Count')
    percentage_df['Percentage'] = (percentage_df['Count'] / len(df)) * 100

    # Define the colors
    colors = ['#1f4462', '#8c8c8c']

    # Create the treemap using Plotly Express
    fig_relation = px.treemap(
        percentage_df,
        path=['Location', 'Caregiver relation to patient'],
        values='Percentage',
        title='Caregiver Relation to Patient by Location (Percentage)',
        color_discrete_sequence=colors
)

    st.plotly_chart(fig_relation,use_container_width=True)



    st.markdown("<h3 style='text-align: left;'>Income of Caregivers</h3>", unsafe_allow_html=True)

    col111,col222 =  st.columns((1,1))

    with col111:

        caregiving_status = ['Caregiving status', 'Indirect caregiver (organizational)', 'Non-caregiver']
        income_rates = [0.1, 0.2, 0.7]  # Example rates for income categories

        fig2 = go.Figure()

        fig2.add_trace(go.Bar(
            x=caregiving_status,
            y=income_rates,
            name='Income',
            marker=dict(color='rgba(58, 71, 80, 0.6)')
))

        fig2.update_layout(
            title='Relationship between Caregiving Status and Income',
            xaxis=dict(title='Caregiving Status'),
            yaxis=dict(title='Income Rate'),
            showlegend=False
)

        st.plotly_chart(fig2,use_container_width=True)


    with col222:

        caregiving_status = ['Direct caregiver (hands-on / partial)', 'Indirect caregiver (organizational)', 'Non-caregiver']
        locations = ['Beirut', 'Aley', 'Chouf']
        income_rates = [0.1, 0.2, 0.7]  # Example rates for income categories

        fig3 = go.Figure()

        fig3.add_trace(go.Bar(
            x=[f"{status}<br>{location}" for status in caregiving_status for location in locations],
            y=income_rates * len(locations),
            name='Income',
            marker=dict(color='rgba(58, 71, 80, 0.6)')
))

        fig3.update_layout(
            title='Relationship between Caregiving Status, Location, and Income',
            xaxis=dict(title='Caregiving Status - Location'),
            yaxis=dict(title='Income Rate'),
            showlegend=False
)

        st.plotly_chart(fig3,use_container_width=True)

    
    st.markdown("<h5 style='text-align: left;'>Age Distribution of Caregivers</h5>", unsafe_allow_html=True)



    # Caregiver age and gender data
    ages = [39, 76, 76, 75, 52, 65, 50, 84, 30, 35, 45, 81, 74, 42, 62, 50, 53, 65, 72, 62, 76, 39, 60,
            42, 48, 45, 47, 60, 84, 48, 72, 82, 60, 51, 65, 63, 49, 63, 55, 60, 55, 32, 70, 82, 72,
            45, 42, 20, 21, 43, 20, 43, 22, 63, 16, 40, 53, 22, 40, 32, 53, 21, 66, 65, 63, 60, 66,
            63, 65, 65, 70, 42, 55, 78]
    genders = ['Male', 'Female', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female',
                'Male', 'Female', 'Male', 'Male', 'Male', 'Female', 'Female', 'Female', 'Female', 'Male', 'Male', 'Male',
                'Male', 'Female', 'Male', 'Female', 'Male', 'Male', 'Male', 'Male', 'Female', 'Male', 'Female', 'Female',
                'Female', 'Male', 'Male', 'Female', 'Male', 'Female', 'Male', 'Male', 'Male', 'Female', 'Male', 'Male',
                'Female', 'Male', 'Male', 'Female', 'Male', 'Female', 'Female', 'Female', 'Female', 'Male', 'Male',
                'Male', 'Female', 'Female', 'Male', 'Male', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female',
                'Male', 'Male']

    # Define the colors
    colors = ['#1f4462', '#8c8c8c']

    # Filter ages for each gender
    male_ages = [age for age, gender in zip(ages, genders) if gender == 'Male']
    female_ages = [age for age, gender in zip(ages, genders) if gender == 'Female']

    # Create the histogram traces for each gender
    trace1 = go.Histogram(x=male_ages, nbinsx=10, marker=dict(color=colors[0]), opacity=0.5, name='Male')
    trace2 = go.Histogram(x=female_ages, nbinsx=10, marker=dict(color=colors[1]), opacity=0.5, name='Female')

    # Define the layout
    layout = go.Layout(
        title='Distribution of Caregiver Ages by Gender',
        xaxis=dict(title='Age'),
        yaxis=dict(title='Frequency'),
        showlegend=True
)

    # Create the figure and add the traces
    fig3 = go.Figure(data=[trace1, trace2], layout=layout)

    #Display the stacked histogram using Streamlit
    st.plotly_chart(fig3,use_container_width=True)



if menu_id== 'Symptoms':

    st.markdown("<h1 style='text-align: center;'>Patient Dementia Symptoms</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: left;'>Physical Symptoms</h3>", unsafe_allow_html=True)


    left1,left2 = st.columns((1,1))

    with left1:


        # Create a DataFrame with the data
        data = {
            'Symptoms': ['Headaches', 'Hands shake', 'Digestion problems', 'Sleep problems'],
            'Yes': [30, 0, 0, 16],
            'No': [70, 100, 100, 84]
}
        df = pd.DataFrame(data)

        # Set the Symptoms column as the index
        df.set_index('Symptoms', inplace=True)

        # Calculate the percentages
        df['Total'] = df['Yes'] + df['No']
        df['Yes %'] = (df['Yes'] / df['Total']) * 100
        df['No %'] = (df['No'] / df['Total']) * 100

        # Round the percentages to two decimal places
        df['Yes %'] = df['Yes %'].round(2)
        df['No %'] = df['No %'].round(2)

        # Define the colors
        colors = ['#1f4462', '#8c8c8c']

        # Create the horizontal bar chart using Plotly
        fig4 = go.Figure()

        # Add the "Yes" bars
        fig4.add_trace(go.Bar(
            y=df.index,
            x=df['Yes %'],
            text=df['Yes'],
            textposition='auto',
            orientation='h',
            name='Yes',
            marker=dict(color=colors[0])
))

        # Add the "No" bars
        fig4.add_trace(go.Bar(
            y=df.index,
            x=df['No %'],
            text=df['No'],
            textposition='auto',
            orientation='h',
            name='No',
            marker=dict(color=colors[1])
))

        # Set the chart title and labels
        fig4.update_layout(
            title='Physical Symptoms',
            xaxis_title='Percentage',
            yaxis_title='Symptoms'
)

        # Streamlit UI components
        st.markdown("<h5 style='text-align: left;'>Physical Symptoms Rates</h5>", unsafe_allow_html=True)
        selected_symptom = st.selectbox('Select a Physical Symptom', options=['All'] + df.index.tolist(), key = 'selectbox1')

        # Filter the DataFrame based on the selected symptom
        if selected_symptom != 'All':
            filtered_df2 = df.loc[[selected_symptom]]
        else:
            filtered_df2 = df

        # Display the filtered chart using Streamlit
        st.plotly_chart(fig4.update_traces(y=filtered_df2.index),use_container_width=True)



    with left2:


        # Symptom data
        symptoms = ['Headaches', 'Hands shake', 'Digestion problems', 'Sleep problems']
        rates = [[0.5, 0.7, 0.6, 0.8], [0.4, 0.6, 0.5, 0.7], [0.3, 0.5, 0.4, 0.6], [0.6, 0.8, 0.7, 0.9]]

        # Create the box plot using Plotly
        fig5 = go.Figure()

        for i in range(len(symptoms)):
            fig5.add_trace(go.Box(
            y=rates[i],
            name=symptoms[i],
            boxpoints='all',
            marker_color='#132a3d',
            line_color='#132a3d'
    ))

        fig5.update_layout(
            title='Distribution of Symptom Severity across Physical Symptoms',
            xaxis=dict(title='Symptoms'),
            yaxis=dict(title='Rates'),
            showlegend=False
)

        # Streamlit UI components
        st.markdown("<h5 style='text-align: left;'>Symptom Severity Analaysis</h5>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("")
        st.plotly_chart(fig5,use_container_width=True)
    



    # Symptom and time period data
    time_periods = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    symptoms = ['Headaches', 'Hands shake', 'Digestion problems', 'Sleep problems']

    rates = [[0.3, 0.4, 0.2, 0.5, 0.3, 0.6],
                [0.2, 0.3, 0.5, 0.4, 0.2, 0.4],
                [0.4, 0.5, 0.3, 0.4, 0.3, 0.5],
                [0.3, 0.2, 0.4, 0.3, 0.5, 0.4]]

    # Create a normalized version of the rates
    normalized_rates = np.array(rates) / np.max(rates)

    # Create the heatmap using Plotly
    fig6 = go.Figure(data=go.Heatmap(
        x=time_periods,
        y=symptoms,
        z=normalized_rates,
        colorscale=[[0, '#8c8c8c'], [1, '#132a3d']],
        reversescale=True,
        zmin=0,
        zmax=1,
        colorbar=dict(
            title='Rates',
            tickformat='.1%',
            tickmode='array',
            tickvals=[0, 0.25, 0.5, 0.75, 1],
                ticktext=['0%', '25%', '50%', '75%', '100%']
    )
))

    fig6.update_layout(
        title='Trends of Physical Symptoms over Time',
        xaxis=dict(title='Time Period'),
        yaxis=dict(title='Symptoms'),
        showlegend=False,
        plot_bgcolor='#132a3d'
)

    # Streamlit UI components
    st.plotly_chart(fig6,use_container_width=True)



    st.markdown("<h3 style='text-align: left;'>Psychological and Emotional Symptoms</h3>", unsafe_allow_html=True)

    left22,right22 = st.columns((2,1))

    with left22:



        # Create a DataFrame with the data
        data = {
                'Symptoms': ['Frightened', 'Nervous, tense or worried', 'Unhappy feelings', 'Crying',
                    'Does not enjoy daily activities', 'Unable to do useful part in life',
                    'Lost interest in things', 'Feel a worthless person', 'Suicidal thoughts',
                    'Tired feelings all time'],
                'Yes': [14, 32, 28, 7, 16, 76, 11, 1, 2, 16],
                'No': [86, 68, 72, 93, 84, 24, 89, 99, 98, 84]
}
        df = pd.DataFrame(data)

        # Set the Symptoms column as the index
        df.set_index('Symptoms', inplace=True)

        # Calculate the percentages
        df['Total'] = df['Yes'] + df['No']
        df['Yes %'] = (df['Yes'] / df['Total']) * 100
        df['No %'] = (df['No'] / df['Total']) * 100

        # Round the percentages to two decimal places
        df['Yes %'] = df['Yes %'].round(2)
        df['No %'] = df['No %'].round(2)

        # Define the colors
        colors = ['#1f4462', '#8c8c8c']

        # Create the horizontal bar chart using Plotly
        fig7 = go.Figure()

        # Add the "Yes" bars
        fig7.add_trace(go.Bar(
            y=df.index,
            x=df['Yes %'],
            text=df['Yes'],
            textposition='auto',
            orientation='h',
            name='Yes',
            marker=dict(color=colors[0])
))

        # Add the "No" bars
        fig7.add_trace(go.Bar(
            y=df.index,
            x=df['No %'],
            text=df['No'],
            textposition='auto',
            orientation='h',
            name='No',
            marker=dict(color=colors[1])
))

        # Set the chart title and labels
        fig7.update_layout(
            title='Psychological and Emotional Symptoms',
            xaxis_title='Percentage',
            yaxis_title='Symptoms'
)

        # Streamlit UI components
        st.plotly_chart(fig7,use_container_width=True)

    
    with right22:

        # Create a DataFrame with the data
        data = {
            'Symptoms': ['Frightened', 'Nervous, tense or worried', 'Unhappy feelings', 'Crying',
                        'Does not enjoy daily activities', 'Unable to do useful part in life',
                        'Lost interest in things', 'Feel a worthless person', 'Suicidal thoughts',
                        'Tired feelings all time'],
            'Yes': [14, 32, 28, 7, 16, 76, 11, 1, 2, 16],
            'No': [86, 68, 72, 93, 84, 24, 89, 99, 98, 84]
}
        df = pd.DataFrame(data)

        # Set the Symptoms column as the index
        df.set_index('Symptoms', inplace=True)

        # Create a list to store the values
        values = []

        # Append 'Yes' values to the list
        values.append(df['Yes'].values)

        # Append 'No' values to the list
        values.append(df['No'].values)

        # Define the colors
        colors = ['#1f4462', '#8c8c8c']

        # Create the box plot using Plotly
        fig8 = go.Figure()

        # Add the box plot traces
        for i in range(len(values)):
            fig8.add_trace(go.Box(
                y=values[i],
                name='Yes' if i == 0 else 'No',
                marker=dict(color=colors[i])
    ))

        # Set the chart title and labels
        fig8.update_layout(
            yaxis_title='Symptoms',
            boxmode='group'  # Display the box plots side by side
)

        # Streamlit UI components
        st.plotly_chart(fig8,use_container_width=True)


    

    # Data
    time_periods = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    symptoms = ['Frightened', 'Nervous, tense or worried', 'Unhappy feelings', 'Crying',
                'Does not enjoy daily activities', 'Unable to do useful part in life',
                'Lost interest in things', 'Feel a worthless person', 'Suicidal thoughts',
                'Tired feelings all the time']

    rates = [[0.3, 0.4, 0.2, 0.5, 0.3, 0.6],
            [0.2, 0.3, 0.5, 0.4, 0.2, 0.4],
            [0.4, 0.5, 0.3, 0.4, 0.3, 0.5],
            [0.3, 0.2, 0.4, 0.3, 0.5, 0.4],
            [0.2, 0.3, 0.4, 0.3, 0.4, 0.2],
            [0.5, 0.4, 0.3, 0.2, 0.3, 0.4],
            [0.3, 0.5, 0.2, 0.4, 0.3, 0.4],
            [0.4, 0.3, 0.5, 0.4, 0.2, 0.3],
            [0.3, 0.4, 0.3, 0.2, 0.4, 0.3],
            [0.4, 0.3, 0.4, 0.3, 0.3, 0.4]]

    # Create a normalized version of the rates
    normalized_rates = np.array(rates) / np.max(rates)

    # Create the heatmap using Plotly
    fig9 = go.Figure(data=go.Heatmap(
        x=time_periods,
        y=symptoms,
        z=normalized_rates,
        colorscale=[[0, '#8c8c8c'], [1, '#132a3d']],
        reversescale=True,
        zmin=0,
        zmax=1,
        colorbar=dict(
            title='Rates',
            tickformat='.1%',
            tickmode='array',
            tickvals=[0, 0.25, 0.5, 0.75, 1],
            ticktext=['0%', '25%', '50%', '75%', '100%']
    )
))

    fig9.update_layout(
        title='Trends of Psychological Symptoms over Time',
        xaxis=dict(title='Time Period'),
        yaxis=dict(title='Symptoms'),
        showlegend=False,
        plot_bgcolor='#132a3d'
)

    # Streamlit UI components
    st.plotly_chart(fig9,use_container_width=True)


    st.markdown("<h3 style='text-align: left;'>Mental and Cognitive Symptoms</h3>", unsafe_allow_html=True)


    # Create a DataFrame with the data
    data = {
        'Symptoms': ['Memory issues', 'Issues to perform activities', 'Thinking problem',
                'Decision making problems', 'Disability to think and reason',
                'Does his/her thinking seem muddled?', 'Mental disorders'],
        'Yes': [66, 14, 9, 8, 10, 15, 25],
        'No': [34, 471, 495, 492, 490, 485, 460]
}
    df = pd.DataFrame(data)

    # Set the Symptoms column as the index
    df.set_index('Symptoms', inplace=True)

    # Calculate the rates
    df['Total'] = df['Yes'] + df['No']
    df['Yes %'] = (df['Yes'] / df['Total']) * 100
    df['No %'] = (df['No'] / df['Total']) * 100

    # Round the percentages to two decimal places
    df['Yes %'] = df['Yes %'].round(2)
    df['No %'] = df['No %'].round(2)

    # Define the colors
    colors = ['#1f4462', '#8c8c8c']

    # Create the horizontal bar chart using Plotly
    fig10 = go.Figure()

    # Add the "Yes" bars
    fig10.add_trace(go.Bar(
        y=df.index,
        x=df['Yes %'],
        text=df['Yes %'],
        textposition='auto',
        orientation='h',
        name='Yes',
        marker=dict(color=colors[0])
))

    # Add the "No" bars
    fig10.add_trace(go.Bar(
        y=df.index,
        x=df['No %'],
        text=df['No %'],
        textposition='auto',
        orientation='h',
        name='No',
        marker=dict(color=colors[1])
))

    # Set the chart title and labels
    fig10.update_layout(
        title='Mental and Cognitive Symptoms',
        xaxis_title='Percentage',
        yaxis_title='Symptoms'
)

    # Streamlit app
    st.plotly_chart(fig10,use_container_width=True)

    


    symptoms = ['Memory issues', 'Issues to perform activities', 'Thinking problem',
                'Decision making problems', 'Disability to think and reason',
                'Does his/her thinking seem muddled?', 'Mental disorders']
    rates = [[0.66], [0.02, 0.05, 0.01], [0.09], [0.08], [0.1], [0.15], [0.04, 0.08, 0.02]]

    fig11 = go.Figure()

    for i in range(len(symptoms)):
        fig11.add_trace(go.Box(
            y=rates[i],
            name=symptoms[i],
            boxpoints='all',
            marker_color='#132a3d',
            line_color='#132a3d'
    ))

    st.markdown("<h5 style='text-align: left;'>Distribution of Symptom Severity across Mental and Cognitive Symptoms</h5>", unsafe_allow_html=True)

    # Streamlit app
    st.plotly_chart(fig11,use_container_width=True)




































