import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.api.sql_connection import create_connection
from app.site.date_utils import date_format_utc
from datetime import datetime
from flask import current_app
from flask_login import current_user


def getPathPlot(current_user, date_i, date_f, showVisits, removeIdle, tripsColor):
    conn = create_connection(current_user)
    date_i = date_format_utc(date_i)
    date_f = date_format_utc(date_f)
    
    query = ('''
    SELECT *
    FROM path
    WHERE timestamp BETWEEN "%s" AND "%s"
    ''' % (str(date_i), str(date_f)))
    df = pd.read_sql(query, conn)

    visits_query = ('''
    SELECT *
    FROM visits
    WHERE (arrival BETWEEN "%s" AND "%s") OR (departure BETWEEN "%s" AND "%s")
    ''' % (str(date_i), str(date_f), str(date_i), str(date_f)))
    df_visits = pd.read_sql(visits_query, conn)

    df['trip'] = 0
    if removeIdle or tripsColor:
        # Remove redundant points and apply color between stops
        i = 0
        df['timestamp_datetime'] = pd.to_datetime(df['timestamp'])
        df_visits['arrival_datetime'] = pd.to_datetime(df_visits['arrival'])
        df_visits['departure_datetime'] = pd.to_datetime(df_visits['departure'])

        for index,row in df_visits.iterrows():
            arrival = row['arrival_datetime']
            departure = row['departure_datetime']
            midTime = arrival + (departure - arrival)/2

            if removeIdle:
                # Delete redundant points
                minuteOffset = 10
                arrivalDel = arrival + pd.Timedelta(minutes=minuteOffset)
                departureDel = departure - pd.Timedelta(minutes=minuteOffset)
                df = df[~((df["timestamp_datetime"] >= arrivalDel) & (df["timestamp_datetime"] <= departureDel))]
            
            if tripsColor:
                # Color trips
                if index == 0:
                    df.loc[df["timestamp_datetime"] < midTime, 'trip'] = i
                    i+=1
                    df.loc[df["timestamp_datetime"] >= midTime, 'trip'] = i
                    i+=1
                elif index == df_visits.index[-1]:
                    df.loc[df["timestamp_datetime"] >= midTime, 'trip'] = i
                    i+=1
                else:
                    # All the cases in between
                    nextArrival = df_visits.iloc[index+1]["arrival_datetime"]
                    nexDeparture = df_visits.iloc[index+1]["departure_datetime"]
                    nextMidTime = nextArrival + (nexDeparture - nextArrival)/2

                    df.loc[(df["timestamp_datetime"] >= midTime) & (df['timestamp_datetime'] < nextMidTime), 'trip'] = i
                    i+=1
    print(df)
                
    # Plot
    fig = px.line_mapbox(df,
    lat="LAT",
    lon="LONG",
    hover_data=["speed","timestamp"],
    color="trip",
    #color_discrete_sequence=["White","Green","Yellow","Red","Pink"],
    zoom=8)

    # Add visits waypoints
    if not df_visits.empty and showVisits:
        fig.add_trace(go.Scattermapbox(
            lat=df_visits["LAT"],
            lon=df_visits["LONG"],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=25,
                color='RoyalBlue',
                opacity=0.7
            ),
            hoverinfo='none'
        ))

    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(showlegend=False)

    return fig


def deleteHomePoints(df, current_user, radius=200):
    try:
        homeLAT = current_user.homeLAT
        homeLON = current_user.homeLONG
        df = df[((abs(df['LAT'] - homeLAT) * 111139) > radius) & ((abs(df['LONG'] - homeLON) * 111139) > radius)]
        missingHome= False
    except:
        missingHome = True
    return df, missingHome


def getVisitsPlot(current_user, date_i, date_f, ignore_home):
    conn = create_connection(current_user)
    date_i = date_format_utc(date_i)
    date_f = date_format_utc(date_f)

    query = ('''
    SELECT *
    FROM visits
    WHERE (arrival BETWEEN "%s" AND "%s") OR (departure BETWEEN "%s" AND "%s")
    ''' % (str(date_i), str(date_f), str(date_i), str(date_f)))

    df = pd.read_sql(query, conn)

    if ignore_home:
        df, missingHome = deleteHomePoints(df, current_user)
    else:
        missingHome = False

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

    return fig, missingHome


if __name__ == '__main__':
    pass