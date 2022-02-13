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

def deleteHomePoints(df, current_user, radius=200):
    homeLAT = current_user.homeLAT
    homeLON = current_user.homeLONG
    df = df[((abs(df['LAT'] - homeLAT) * 111139) > radius) & ((abs(df['LONG'] - homeLON) * 111139) > radius)]
    return df

def getPlot(current_user, date_i, date_f, ignore_home=False):
    db_name = current_user.username + '.db'
    db_path = pathlib.Path.cwd() / 'database' / db_name
    conn = create_connection(db_path)

    query = ('''
    SELECT *
    FROM visits
    WHERE arrival BETWEEN "%s" AND "%s"
    ''' % (str(date_i), str(date_f)))
    print(query)
    df = pd.read_sql(query, conn)

    if ignore_home == 'true':
        df = deleteHomePoints(df, current_user)

    # Plot
    fig = px.density_mapbox(df, 
    lat='LAT', 
    lon='LONG',
    z='duration',
    zoom=1,
    height=500,
    hover_data=["arrival","departure"])
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

if __name__ == '__main__':
    pass