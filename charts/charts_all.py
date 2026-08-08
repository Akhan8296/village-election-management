import plotly.express as px

def create_gender_chart(df):
    fig = px.pie(df, names="GENDER", values="VOTER_COUNT", title="Gender Distribution", hole=0.3)
    fig.update_traces(textinfo="percent+label")
    return fig

def create_age_chart(df):
    fig = px.bar(
        df,
        x="AGE_GROUP",
        y="VOTER_COUNT",
        title="Voter Age Distribution",
        text="VOTER_COUNT"
    )
    return fig