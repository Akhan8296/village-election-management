import streamlit as st
from services.dashboard_service import get_gender_data
from charts.gender_charts import create_gender_chart

def show_dashboard():
    st.title("Election Dashboard")
    df_gender = get_gender_data()
    fig = create_gender_chart(df_gender)
    st.plotly_chart(
        fig,
        use_container_width=True
    )