import streamlit as st
from services.dashboard_service import get_gender_data
from services.dashboard_service import get_age_data
from charts.charts_all import create_gender_chart
from charts.charts_all import create_age_chart
from services.dashboard_service import get_house_data
from charts.charts_all import create_house_chart

def show_dashboard():
    st.title("Election Dashboard")
    st.markdown("""
    <style>
    .chart-box {
        border: 2px solid black;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Get data
    df_gender = get_gender_data()
    df_age = get_age_data()
    df_house = get_house_data()

    # Create charts
    gender_fig = create_gender_chart(df_gender)
    gender_fig.update_layout(height=250)
    age_fig = create_age_chart(df_age)
    age_fig.update_layout(height=250)

    house_fig = create_house_chart(df_house)
    house_fig.update_layout(height=250)

    # Display side by side
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.plotly_chart(gender_fig, use_container_width=True)

    with col2:
        with st.container(border=True):
            st.plotly_chart(age_fig, use_container_width=True)

    with st.container(border=True):
        st.plotly_chart(house_fig, use_container_width=True)
    