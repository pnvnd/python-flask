from flask import Blueprint, render_template



# Flask Blueprint Application
covid2 = Blueprint("covid2", "covid2")

@covid2.route("/projects/covid2", strict_slashes=False)
def main():
    import urllib.request
    import pandas as pd
    import plotly.offline as pyo
    import plotly.graph_objs as go

    source = "https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv"
    df = pd.read_csv(urllib.request.urlopen(source))

    list = df.columns[1:]

    data = []

    for item in list:
        trace = go.Scatter(x=df["Reported Date"], y=df[item], mode="lines", name=item)
        data.append(trace)

    layout = go.Layout(title="Ontario COVID Data")

    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig, filename="datacrunch-consulting/templates/projects/covid2.html", auto_open=False)
    return render_template("projects/covid2.html", title="Ontario COVID-19")