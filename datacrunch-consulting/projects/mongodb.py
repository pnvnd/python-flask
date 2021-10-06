from pywebio import *
from pywebio.output import *
from pywebio.input import *
from pywebio.pin import *
from pywebio.session import hold
from pymongo import MongoClient

def mongodbApp():
    # Change favicon.ico
    # run_js("$('head link[rel=icon]').attr('href', image_url)", image_url="../../favicon.ico")

    # Initial Popup message
    # popup("Terms of Service", [
    #     put_text("Access authorized for employees only. This system is monitored and uses cookies."),
    #     put_buttons(["Agree"], onclick=lambda _: close_popup())
    #     ])

    #Start Session
    attempts = 0
    if attempts > 1: return put_markdown("# Not authorized!")
    try:
        # Login Page
        credentials = input_group("MongoDB Portal", [
        input("Username", name="username"),
        input("Password", name="password",
            type=PASSWORD,
            placeholder="Enter your password",
            help_text="Please contact IT Support for access.",
            required = True
            ),
        radio("Environment", options=["PROD", "QA", "DEV"], value="PROD", inline=True, required=True, name="env")
        ])

        with put_loading(shape="border", color="dark"):
            
            username = credentials.get("username")
            password = credentials.get("password")

            global env, database, cluster, db
            env = credentials.get("env")
            database = "sample_analytics" #Auth database

            if env == "PROD":
                host = "cluster0.q2imb.mongodb.net/"
            elif env =="QA":
                host = "db.qa.mongodb.net/"
            elif env == "DEV":
                host = "db.dev.mongodb.net/"

            uri = ("mongodb+srv://" + username + ":" + password + "@" + host + database)
            cluster = MongoClient(uri)
            db = cluster[database]

            collections = db.list_collection_names()
        
        hold()
            
    except:
        attempts+=1
        toast("Incorrect username, password, and environment combination.", color="error")
        session(attempts)

    else:
        toast("Successfully connected to " + env, color="success")
        put_markdown("# MongoDB Portal")
        put_markdown("## Customer Lookup")
        put_input("accounts", type=NUMBER)
        put_buttons(["Lookup"], lambda _: lookupAccounts(pin.accounts))
    
    hold()

# Try account_number = 371138
def lookupAccounts(account_number):
    with use_scope("search_result", clear=True):
        with put_loading(shape="border", color="dark"):
            customers = db.customers

            # Search pipeline for customers collection in MongoDB
            pipeline = [
                { "$match" : 
                    { "$and" : [
                        { "accounts": account_number }, 
                    ]}
                },
                { "$project" : { "_id": 0 } } # Show everything except _id field
            ]

            import pandas as pd
            data = pd.DataFrame(list(customers.aggregate(pipeline)))
            columns = data.columns.tolist()
            rows = data.values.tolist()
            
            # Show interactive data visualizations
            from pywebio.output import put_html
            import plotly.graph_objects as go
           
            fig = go.Figure(data=[go.Table(header=dict(values=["Customer Info"]), cells=dict(values=rows))])
            html = fig.to_html(include_plotlyjs="require", full_html=False)
            put_html(html)
    hold()
         