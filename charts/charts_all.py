import plotly.express as px

def create_gender_chart(df):
    fig = px.pie(df, names="GENDER", values="VOTER_COUNT", title="Gender Distribution", hole=0.3)
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(height=350, shapes=[dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))])
    return fig

def create_age_chart(df):
    fig = px.bar(df,x="AGE_GROUP",y="VOTER_COUNT",title="Voter Age Distribution",text="VOTER_COUNT")
    fig.update_layout(height=350, shapes=[dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))])
    return fig

def create_house_chart(df):
    fig = px.line(df,x="HOUSE_NO",y="VOTER_COUNT",title="Voters by House Number",markers=True)
    fig.update_layout(height=350, shapes=[dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))])
    return fig