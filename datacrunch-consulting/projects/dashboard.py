from dash import dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

def init_dashboard(server):
    dashapp = dash.Dash(
        server=server,
        routes_pathname_prefix="/projects/dashapp/"
        # external_stylesheets=[
        #     "/static/styles.css",
        #     "https://fonts.googleapis.com/css?family=Lato",
        # ],
    )

    url = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv'
    df = pd.read_csv(url)

    dashapp.layout = html.Div([
        dcc.Graph(id='graphs'),
        dcc.Dropdown(id='option-picker', options=[{"label": x, "value": x} for x in df.columns[1:]], value=df.columns[1])
    ])

    @dashapp.callback(Output('graphs', 'figure'), [Input('option-picker', 'value')])
    def update_figure(selected_option):   
        return {
            'data': [go.Scatter(x=df['Reported Date'], y=df[selected_option], mode='lines')],
            'layout': go.Layout(title='COVID Data', xaxis={'title': 'Date'}, yaxis={'title': 'Number of Cases'})
        }

    return dashapp.server