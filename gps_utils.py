from pathlib import Path
import json
import pandas as pd
import numpy as np
from pathlib import Path


def get_user_dir(user_id):
    dir = Path.cwd()
    return dir/'storage'/user_id


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


def checkins(df, user_id):
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
        last_checkin = df_checkins.iloc[-1].to_dict()

        # Write json
        checkin_filepath = get_user_dir(user_id) / user_id+'_checkin.json'
        with open(checkin_filepath,'w') as file:
            # Write json file
            json.dump(last_checkin, file, indent = 4)
    
    return True


def visits(df, user_id):
    
    df_visits = df[(df['properties_action'] == 'visit') & (df['properties_departure_date'].notna())]

    visits_cols = ['geometry_coordinates_0', 'geometry_coordinates_1', 'properties_arrival_date', 'properties_departure_date','properties_device_id']
    df_visits = df_visits[visits_cols].reset_index(drop=True)
    df_visits.columns = ['LONG','LAT','arrival','departure','device']

    if df_visits.empty:
        pass
    else:
        csv_path = get_user_dir(user_id) / user_id+'_visits.csv'
        df_visits.to_csv(csv_path, mode='a', header=False, index=False)
    return True


def min(df, user_id, accuracy=10, desired_distance=50, stationary=True):
    '''
    Generates a much smaller dataframe with fewer GPS points.

    accuracy =          Accuracy of the GPS point measurement
    desired_distance =  Minimum distance between each GPS point
    stationary =        False if it wants to delete stationary points

    Useful to process data later in a web app
    '''

    # Get only interesting properties for map plotting
    columns = ['geometry_coordinates_0', 'geometry_coordinates_1', 'properties_altitude', 'properties_speed', 'properties_timestamp', 'properties_vertical_accuracy', 'properties_horizontal_accuracy', 'properties_motion_0']
    df2 = df[columns]

    # Get rid of stationary points
    if not stationary:
        df2 = df2[~df2['properties_motion_0'].isin(['stationary'])]

    # Get rid of points without motion data
    df2 = df2[df2['properties_motion_0'].notna()]

    # Get rid of unnacurate points (accuracy < 10m)
    df2 = df2[df2['properties_horizontal_accuracy'] < accuracy]

    # Rename columns
    df2.columns = ['LONG','LAT','ALT','speed','timestamp','vertical_accuracy','horizontal_accuracy','motion']
    df2 = df2.reset_index(drop=True)

    # Remove points that are too close together
    df_min = pd.DataFrame(columns=df2.columns)  # Empty dataframe to append desired values
    last_coords=[]

    for index, row in df2.iterrows():
        # Skip index 0
        if index > 0:
            lat1 = last_coords['LAT']
            long1 = last_coords['LONG']
            lat2 = row['LAT']
            long2 = row['LONG']
            distance = haversine(lat1,long1,lat2,long2)  # Distance in meters between two points

            if distance > desired_distance:
                df_min = df_min.append(row)
                last_coords = {'LAT':row['LAT'],'LONG':row['LONG']}
            else:
                pass
        else:
            df_min = df_min.append(row)
            last_coords = {'LAT':row['LAT'],'LONG':row['LONG']}
    
    file = user_id+'_min.csv'
    csv_path = get_user_dir(user_id) / file
    df_min.to_csv(csv_path, mode='a', header=False, index=False)

    return True


def main_csv(df, user_id):
    # Writes main CSV
    file = user_id+'.csv'
    filepath = get_user_dir(user_id) / file

    df.to_csv(filepath, mode='a', header=False, index=False)


if __name__ == "__main__":
    lat1 = 40.7128
    long1 = 74.0060
    lat2 = 51.5072
    long2 = 0.1276
    distance = haversine(lat1,long1,lat2,long2)
    print("Distance = %s meters" % round(distance,2))