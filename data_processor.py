import os
import json
import pandas as pd
from pathlib import Path

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

def directories(user_id):
    # Get or create user files
    # User directory
    user_directory = 'storage/'+user_id+'/'
    Path(user_directory).mkdir(parents=True, exist_ok=True)
    # User's json file to store raw data if desired
    user_json = Path(user_directory+user_id+'.json')
    user_json.touch(exist_ok=True)
    # User's csv file to store locations
    user_csv = Path(user_directory+user_id+'.csv')
    user_csv.touch(exist_ok=True)

    return user_json, user_csv

def write_json(user_json, content):
    # Handle new files
    if os.path.getsize(user_json) == 0:
        new_data = {}
        with open(user_json,'r+') as file:
            file.write(json.dumps(new_data))

    # Append json data
    with open(user_json,'r+') as file:
        # new_data = json.dumps(content, indent=4)
        new_data = content
        file_data = json.load(file)
        # Get id of last writen data
        keys = list(file_data.keys())
        new_key = str(int(keys[-1]) + 1) if len(keys) > 0 else "0"
        file_data[new_key] = new_data
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def write_csv(user_csv, content):
    # CSV data
    current_df = pd.DataFrame([flatten_json(x) for x in content['locations']])
    if os.path.getsize(user_csv) == 0:
        new_data = current_df.columns.values.tolist()
        with open(user_csv,'r+') as file:
            file.write(','.join(new_data))
    df = pd.read_csv(user_csv)
    df = pd.concat([df, current_df], axis=0)
    df.to_csv(user_csv, index=False)

def handle_data(user_id, content):
    user_json, user_csv = directories(user_id)
    write_json(user_json, content)
    write_csv(user_csv, content)

    return True


if __name__ == "__main__":
    pass