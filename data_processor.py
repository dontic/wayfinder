import pandas as pd
from pathlib import Path
import json
import sql_connection
import sql_dump


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


def write_json(user_id, content):
    file = user_id+'_last.json'
    filepath = Path.cwd()/'storage'/file
    with open(filepath,'w') as file:
        json.dump(content, file, indent = 4)


def get_df(user_id, content):
    # Get dataframe from json
    df_content = pd.DataFrame([flatten_json(x) for x in content['locations']])

    # Ensure all columns are present
    df = pd.DataFrame(columns=['type','geometry_type','geometry_coordinates_0','geometry_coordinates_1','properties_speed','properties_battery_state','properties_timestamp','properties_battery_level','properties_vertical_accuracy','properties_pauses','properties_horizontal_accuracy','properties_wifi','properties_deferred','properties_significant_change','properties_locations_in_payload','properties_activity','properties_device_id','properties_altitude','properties_desired_accuracy','properties_motion_0','properties_action','properties_motion_1','properties_arrival_date','properties_departure_date'])
    df = df.append(df_content)

    '''
    Checks for duplicate points
    If a user stays in the same spot for hours, multiple points might be gathered
    Only interested in first (arrival) and last one (departure)
    

    df_clean = pd.DataFrame(columns=df.columns)  # Empty dataframe to append desired values
    last=[]
    for index, row in df.iterrows():
        if index > 0:
            current = [row['geometry_coordinates_0'],row['geometry_coordinates_1'],row['properties_motion_0']]
            if current != last:  # If the row is different
                df_clean = df_clean.append(last_row)
                df_clean = df_clean.append(row)
                last = [row['geometry_coordinates_0'],row['geometry_coordinates_1'],row['properties_motion_0']]
                last_row = row

            else:
                pass
        else:
            df_clean = df_clean.append(row)
            last = [row['geometry_coordinates_0'],row['geometry_coordinates_1'],row['properties_motion_0']]
            last_row = row
    
    df = df_clean
    '''

    return df


def data_processor(user_id, content):
    
    write_json(user_id, content)  # Saves a copy of the last received content
    df = get_df(user_id, content)  # Gets df from json content

    sql_connection.main(user_id)  # Creates a new sql connection

    # Gather other GPS data
    gps_utils.checkins(df, user_id)
    gps_utils.visits(df, user_id)
    gps_utils.min(df, user_id)
    gps_utils.main_csv(df, user_id)

    return True


if __name__ == "__main__":
    pass