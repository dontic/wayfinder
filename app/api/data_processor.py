from sys import getdefaultencoding
import pandas as pd
pd.options.mode.chained_assignment = None  # default = 'warn'
import numpy as np
from pathlib import Path
import json
from app.api import sql_connection


def flatten_json(nested_json, exclude=['']):
    """Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
            exclude: Keys to exclude from output.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude: flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


def backup_received_json(user, content):
    file = user.username + '_last.json'
    filepath = Path.cwd()/'database'/file
    with open(filepath,'w') as file:
        json.dump(content, file, indent = 4)


def get_df(content):
    # Get dataframe from json
    df_content = pd.DataFrame([flatten_json(x) for x in content['locations']])

    # Ensure all columns are present
    df = pd.DataFrame(columns=['type','geometry_type','geometry_coordinates_0','geometry_coordinates_1','properties_speed','properties_battery_state','properties_timestamp','properties_battery_level','properties_vertical_accuracy','properties_pauses','properties_horizontal_accuracy','properties_wifi','properties_deferred','properties_significant_change','properties_locations_in_payload','properties_activity','properties_device_id','properties_altitude','properties_desired_accuracy','properties_motion_0','properties_action','properties_motion_1','properties_arrival_date','properties_departure_date'])
    df = pd.concat([df, df_content])
    df = df.drop_duplicates()

    df['properties_timestamp'] = pd.to_datetime(df['properties_timestamp'])
    df['properties_arrival_date'] = pd.to_datetime(df['properties_arrival_date'])
    df['properties_departure_date'] = pd.to_datetime(df['properties_departure_date'])

    return df


def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371000):
    """
    slightly modified version: of http://stackoverflow.com/a/29546836/2901002

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.

    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = np.sin((lat2-lat1)/2.0)**2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2

    return earth_radius * 2 * np.arcsin(np.sqrt(a))


def raw_sql_dump(df, conn):
    # Appends main raw data to the SQL database
    df.to_sql(name='raw', con=conn, if_exists='append', index=False)

    return True


def path_sql_dump(df, conn):
    # Columns
    cols = ["geometry_coordinates_0",
    "geometry_coordinates_1",
    "properties_altitude",
    "properties_speed",
    "properties_timestamp",
    "properties_vertical_accuracy",
    "properties_horizontal_accuracy",
    "properties_device_id",
    "properties_motion_0"]

    df = df[cols]

    df.columns = ['LONG','LAT','ALT','speed','timestamp','horizontal_accuracy','vertical_accuracy','device','motion']
    df = df[df['motion'].notna()]
    df["speed"] = 3.6 * df["speed"]  # Speed to KMH
    df = df[df["horizontal_accuracy"] < 50]  # Getting rid of low accuracy points
    
    df.to_sql(name='path', con=conn, if_exists='append', index=False)
    
    return df


def path_min_sql_dump(df_path, conn, accuracy=10, desired_distance=50, remove_stationary=True):
    '''
    Generates a much smaller dataframe with fewer GPS points.
    This is intended for faster plotting.

    accuracy =          Accuracy of the GPS point measurement
    desired_distance =  Minimum distance between each GPS point
    stationary =        False if it wants to delete stationary points

    Useful to process data later in a web app
    '''
    df = df_path
    # Get rid of stationary points
    if remove_stationary:
        df = df[~df['motion'].isin(['stationary'])]

    # Get rid of points without motion data
    df = df[df['motion'].notna()]

    # Get rid of inaccurate points (default accuracy < 10m)
    df = df[df['horizontal_accuracy'] < accuracy]

    # Reset index
    df = df.reset_index(drop=True)

    # Remove points that are too close together
    df_min = pd.DataFrame(columns=df.columns)  # Empty dataframe to append desired values
    last_coords=[]

    for index, row in df.iterrows():
        # Skip index 0
        if index > 0:
            lat1 = last_coords['LAT']
            long1 = last_coords['LONG']
            lat2 = row['LAT']
            long2 = row['LONG']
            distance = haversine(lat1,long1,lat2,long2)  # Distance in meters between two points

            if distance > desired_distance:
                df_min = pd.concat([df_min, row])
                last_coords = {'LAT':row['LAT'],'LONG':row['LONG']}
            else:
                pass
        else:
            df_min = pd.concat([df_min, row])
            last_coords = {'LAT':row['LAT'],'LONG':row['LONG']}
    
    df.to_sql(name='path_min', con=conn, if_exists='append', index=False)

    return True


def visits(df, conn):
    
    df_visits = df[(df['properties_action'] == 'visit') & (df['properties_departure_date'].notna())]

    visits_cols = ['geometry_coordinates_0', 'geometry_coordinates_1', 'properties_arrival_date', 'properties_departure_date','properties_device_id']
    df_visits = df_visits[visits_cols].reset_index(drop=True)
    df_visits.columns = ['LONG','LAT','arrival','departure','device']

    if df_visits.empty:
        pass
    else:
        df_visits['duration'] = (df_visits.departure - df_visits.arrival) / pd.Timedelta(hours=1)
        df_visits.to_sql(name='visits', con=conn, if_exists='append', index=False)

    return True


def checkins(df, user):
    '''
    Gets the last check-in location of the user and stores it in last_checkin.json
    '''

    df_checkins = df[(df['properties_action'] == 'visit') & (df['properties_departure_date'].isna())]

    if df_checkins.empty:
        # No other check-ins since last check-in
        pass
    else:
        # New check-ins found
        checkin_cols = ['geometry_coordinates_0', 'geometry_coordinates_1', 'properties_arrival_date','properties_device_id']
        df_checkins = df_checkins[checkin_cols].reset_index(drop=True)
        df_checkins['properties_arrival_date'] = df_checkins['properties_arrival_date'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')
        last_checkin = df_checkins.iloc[-1].to_dict()

        # Write json
        file = user.username+'_checkin.json'
        filepath = Path.cwd()/'database'/file
        with open(filepath,'w') as file:
            # Write json file
            json.dump(last_checkin, file, indent = 4)
    
    return True


def data_processor(user, content):
    # Main processor for the received data
    print("Backing up received JSON data...")
    backup_received_json(user, content)  # Saves a copy of the last received content
    print("Generating dataframe from received JSON data...")
    df = get_df(content)  # Gets df from json content

    # Create SQL connection
    print("Creting SQL connection with %s's database..." % user.name)
    conn = sql_connection.create_connection(user)  # Creates a .db and tables if they don't exist

    # Dump received raw data to the 'raw' SQL table
    print("Processing raw data...")
    raw_sql_dump(df, conn)

    # Process and dump path data to the 'path' SQL table
    print("Processing path data...")
    df_path = path_sql_dump(df, conn)

    # Process and dump path minimized data to the 'path_min' SQL table
    print("Processing minimized path data...")
    path_min_sql_dump(df_path, conn, accuracy=10, desired_distance=50, remove_stationary=True)

    # Dump new visits to the 'visits' SQL table
    print("Processing visits...")
    visits(df, conn)

    # Save the user's last checkin in json form
    print("Processing last checkin...")
    checkins(df, user)

    return True


if __name__ == "__main__":
    # Test
    from werkzeug.security import generate_password_hash, check_password_hash
    from app.auth.models import User
    user = User(name='Name', email='example@email.com', username='username', password=generate_password_hash('password', method='sha256'), apikey=generate_password_hash('apikey', method='sha256'))
    
    filename = user.username + '_last.json'
    with open(filename, "r") as f:
        content = json.load(f)
    
    df = get_df(user, content)