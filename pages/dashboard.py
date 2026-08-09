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
        <style> [data-testid="column"] { border: 1px solid #ddd; padding: 10px; border-radius: 8px;} </style>
        """, unsafe_allow_html=True)

    # Get data
    df_gender = get_gender_data()
    df_age = get_age_data()
    df_house = get_house_data()

    # Create charts
    gender_fig = create_gender_chart(df_gender)
    gender_fig.update_layout(height=150)
    age_fig = create_age_chart(df_age)
    age_fig.update_layout(height=350)

    house_fig = create_house_chart(df_house)
    house_fig.update_layout(height=350)

    # Display side by side
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(gender_fig, use_container_width=True)
    with col2:
        st.plotly_chart(age_fig,use_container_width=True)
        
    st.plotly_chart(house_fig,use_container_width=True)
    