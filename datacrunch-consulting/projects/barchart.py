from dash import dash, dcc, html
import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd

def init_barchart(server):
    dashapp = dash.Dash(
        server=server,
        routes_pathname_prefix="/projects/barchart/"
        # external_stylesheets=[
        #     "/static/styles.css",
        #     "https://fonts.googleapis.com/css?family=Lato",
        # ],
    )

    app = dash.Dash()

    url = "https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv"
    df = pd.read_csv(url)

    Age_Group = df["Age_Group"].unique().tolist()
    Age_Group.sort()

    Client_Gender = df["Client_Gender"].unique().tolist()

    data = []
    for gender in df["Client_Gender"].unique():
        globals()["count_" + gender] = []

    for gender in Client_Gender:
        for age in Age_Group:
            globals()["count_" + gender].append(df[(df["Age_Group"]==age) & (df["Client_Gender"]==gender)]["Client_Gender"].count())
        
        trace = go.Bar(x=Age_Group, y=globals()["count_" + gender], name=gender)
        data.append(trace)

    colors = {
        "background": "#111111",
        "text":"#7FDBFF"
    }

    layout = go.Layout(
        title="Ontario COVID-19 Case Breakdown by Age Group and Gender",
        xaxis={"title": "Age Group"},
        yaxis={"title": "Number of Cases"}
    )

    dashapp.layout = html.Div(children=[
        html.H1("COVID Data",
            style={
                "textAlign": "center",
                "color": colors["text"]
            }),
        dcc.Graph(
            id="conposcovidloc",
            figure = {
                "data": data,
                "layout": layout
            }
        )]
    )

    return dashapp.server