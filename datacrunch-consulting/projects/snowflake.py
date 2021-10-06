# Import packages
from flask import Blueprint, render_template, request
from snowflake import connector
import json
import pandas as pd

# Credentials
file = open("credentials", "r")
credentials = json.load(file)
file.close()

# Snowflake
cnx = connector.connect(
    account = credentials["account"],
    user = credentials["user"],
    password = credentials["password"],
    warehouse = credentials["warehouse"],
    database = credentials["database"],
    schema = credentials["schema"],
    role = "SYSADMIN")

# Flask Blueprint Application
snowflakeApp = Blueprint("snowflakeApp", "snowflakeApp")

@snowflakeApp.route("/projects/snowflake/")
def main():
    cur = cnx.cursor().execute("select color_name, count(*) "
                                "from colors "
                                "group by color_name "
                                "having count(*) > 50 "
                                "order by count(*) desc;")

    rows = pd.DataFrame(cur.fetchall(), columns=["Color Name", "Votes"])
    dfhtml = rows.to_html(index=False)
    return render_template("/projects/snowflake/index.html", dfhtml=dfhtml)

@snowflakeApp.route("/projects/snowflake/submit")
def submit():
    return render_template("/projects/snowflake/submit.html")

@snowflakeApp.route("/projects/snowflake/thanks4submit", methods=["POST"])
def thanks():
    colorname = request.form.get("cname")
    username = request.form.get("uname")
    cnx.cursor().execute("insert into colors (color_uid, color_name) " +
                         "select color_uid_seq.nextval, '" + colorname + "'")
    return render_template("/projects/snowflake/thanks4submit.html", colorname=colorname, username=username)

@snowflakeApp.route("/projects/snowflake/charts")
def charts():
    cur = cnx.cursor().execute("select color_name, count(*) "
                                "from colors "
                                "group by color_name "
                                "order by count(*) desc;")
    data4charts = pd.DataFrame(cur.fetchall(), columns=["color", "votes"])
    #data4charts.to_csv("data4charts.csv", index=False)
    data4ChartsJSON = data4charts.to_json(orient="records")
    return render_template("/projects/snowflake/charts.html", data4ChartsJSON=data4ChartsJSON)



# #print(rows)
# #onerow = cur.fetchone()
# # test dataframe as html
# #print(dfhtml)