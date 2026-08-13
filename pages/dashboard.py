import streamlit as st
from services.dashboard_service import (get_gender_data, get_age_data, get_house_data, get_gender_age_data, get_kpi_data)
from charts.charts_all import (create_gender_chart, create_age_chart, create_house_chart, create_gender_age_chart)

def show_dashboard():
    st.markdown("""
    <h2 style="
        font-size: 28px;
        margin-top: -25px;
        margin-bottom: 10px;
        font-weight: 600;
    ">
        Data Dashboard
    </h2>
    """, unsafe_allow_html=True)

    # Get data
    df_gender = get_gender_data()
    df_age = get_age_data()
    df_house = get_house_data()
    df_gender_age = get_gender_age_data()
    kpi = get_kpi_data()
    
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        with st.container(border=True):
            st.metric("👥 Total Voters", int(kpi["TOTAL_VOTERS"]))

    with kpi2:
        with st.container(border=True):
            st.metric("♂️ Male Voters", int(kpi["MALE_VOTERS"]))

    with kpi3:
        with st.container(border=True):
            st.metric("♀️ Female Voters", int(kpi["FEMALE_VOTERS"]))

    with kpi4:
        with st.container(border=True):
            st.metric("🏠 Total Houses", int(kpi["TOTAL_HOUSES"]))

    with kpi5:
        with st.container(border=True):
            st.metric("🎂 Average Age", f'{kpi["AVG_AGE"]:.1f}')
    # Create charts
    gender_fig = create_gender_chart(df_gender)
    gender_fig.update_layout(height=250 ,margin=dict(l=0, r=0, t=50, b=30))
    age_fig = create_age_chart(df_age)
    age_fig.update_layout(height=250 ,margin=dict(l=0, r=0, t=50, b=30))

    house_fig = create_house_chart(df_house)
    house_fig.update_layout(height=300 ,margin=dict(l=0, r=0, t=50, b=30))

    gender_age_fig = create_gender_age_chart(df_gender_age)
    gender_age_fig.update_layout(xaxis_title="Age Group", yaxis_title="Number of Voters", height=250 ,margin=dict(l=0, r=0, t=50, b=30))

    # Display side by side
    col1, col2 ,col3= st.columns(3)

    with col1:
        with st.container(border=True):
            st.plotly_chart(gender_fig, width='stretch')

    with col2:
        with st.container(border=True):
            st.plotly_chart(age_fig, width='stretch')

    with col3:
        with st.container(border=True):
            st.plotly_chart(gender_age_fig, width='stretch')

    with st.container(border=True):
        st.plotly_chart(house_fig, width='stretch')
    