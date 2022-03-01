import pandas as pd
import plotly.express as px
from app.api.sql_connection import create_connection
from app.site.date_utils import date_format_utc


def getPathPlot(current_user, date_i, date_f):
    conn = create_connection(current_user)
    date_i = date_format_utc(date_i)
    date_f = date_format_utc(date_f)
    
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
    zoom=8)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


def deleteHomePoints(df, current_user, radius=200):
    homeLAT = current_user.homeLAT
    homeLON = current_user.homeLONG
    df = df[((abs(df['LAT'] - homeLAT) * 111139) > radius) & ((abs(df['LONG'] - homeLON) * 111139) > radius)]
    return df


def getVisitsPlot(current_user, date_i, date_f, ignore_home=False):
    conn = create_connection(current_user)
    date_i = date_format_utc(date_i)
    date_f = date_format_utc(date_f)

    query = ('''
    SELECT *
    FROM visits
    WHERE arrival BETWEEN "%s" AND "%s"
    ''' % (str(date_i), str(date_f)))

    df = pd.read_sql(query, conn)

    if ignore_home == 'true':
        df = deleteHomePoints(df, current_user)

    # Plot
    fig = px.density_mapbox(df, 
    lat='LAT', 
    lon='LONG',
    z='duration',
    zoom=1,
    hover_data=["arrival","departure"])
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(coloraxis_showscale=False)

    return fig


if __name__ == '__main__':
    pass