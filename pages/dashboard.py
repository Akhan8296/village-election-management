import streamlit as st
from services.dashboard_service import get_gender_data
from services.dashboard_service import get_age_data
from charts.charts_all import create_gender_chart
from charts.charts_all import create_age_chart
from services.dashboard_service import get_house_data
from charts.charts_all import create_house_chart
from services.dashboard_service import get_gender_age_data
from charts.charts_all import create_gender_age_chart

def show_dashboard():
    st.title("Election Dashboard")
    st.markdown("""
    <style>
    .chart-box {
        border: 2px solid black;
        border-radius: 8px;
        padding: 2px;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Get data
    df_gender = get_gender_data()
    df_age = get_age_data()
    df_house = get_house_data()
    df_gender_age = get_gender_age_data()

    # Create charts
    gender_fig = create_gender_chart(df_gender)
    gender_fig.update_layout(height=250)
    age_fig = create_age_chart(df_age)
    age_fig.update_layout(height=250 ,margin=dict(l=30, r=20, t=50, b=30))

    house_fig = create_house_chart(df_house)
    house_fig.update_layout(height=300 ,margin=dict(l=30, r=20, t=50, b=30))

    gender_age_fig = create_gender_age_chart(df_gender_age)
    gender_age_fig.update_layout(xaxis_title="Age Group", yaxis_title="Number of Voters", height=250 ,margin=dict(l=30, r=20, t=50, b=30))

    # Display side by side
    col1, col2 ,col3= st.columns(3)

    with col1:
        with st.container(border=True):
            st.plotly_chart(gender_fig, use_container_width=True)

    with col2:
        with st.container(border=True):
            st.plotly_chart(age_fig, use_container_width=True)

    with col3:
        with st.container(border=True):
            st.plotly_chart(gender_age_fig, use_container_width=True)

    with st.container(border=True):
        st.plotly_chart(house_fig, use_container_width=True)
    