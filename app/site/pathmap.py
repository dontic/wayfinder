import sqlite3 as sql
import pathlib
from sqlite3 import Error
import pandas as pd
import plotly.express as px

def create_connection(db_file):
    conn = None
    try:
        conn = sql.connect(db_file)
    except Error as e:
        print(e)
    return conn

def getPlot(current_user, date_i, date_f):
    db_name = current_user.username + '.db'
    print(db_name)
    db_path = pathlib.Path.cwd() / 'database' / db_name
    conn = create_connection(db_path)
    
    query = ('''
    SELECT *
    FROM path
    WHERE timestamp BETWEEN "%s" AND "%s"
    ''' % (str(date_i), str(date_f)))
    df = pd.read_sql(query, conn)

    # Plot
    fig = px.line_mapbox(df,
    lat="LAT",
    lon="LONG",
    hover_data=["speed","timestamp"],
    #color=df["speed_range"],
    #color_discrete_sequence=["White","Green","Yellow","Red","Pink"],
    zoom=8,
    height=500)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

if __name__ == '__main__':
    pass