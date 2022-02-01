from pathlib import Path
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    create a database connection to the SQLite database
    specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """
    create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main(user_id):
    # Path for the user's database
    database_path = Path.cwd() / 'database' / user_id

    sql_create_raw_table = """ CREATE TABLE IF NOT EXISTS raw (
        type TEXT,
        geometry_type TEXT,
        geometry_coordinates_0 FLOAT,
        geometry_coordinates_1 FLOAT,
        properties_speed INT,
        properties_battery_state TEXT,
        properties_timestamp DATETIME,
        properties_battery_level FLOAT,
        properties_vertical_accuracy INT,
        properties_pauses TEXT,
        properties_horizontal_accuracy INT,
        properties_wifi TEXT,
        properties_deferred INT,
        properties_significant_change INT,
        properties_locations_in_payload INT,
        properties_activity TEXT,
        properties_device_id TEXT,
        properties_altitude INT,
        properties_desired_accuracy INT,
        properties_motion_0 TEXT,
        properties_action TEXT,
        properties_motion_1 TEXT,
        properties_arrival_date DATETIME,
        properties_departure_date DATETIME
        );
    """

    sql_create_path_table = """ CREATE TABLE IF NOT EXISTS path (
        LONG FLOAT,
        LAT FLOAT,
        ALT INT,
        speed INT,
        timestamp DATETIME,
        horizontal_accuracy INT,
        vertical_accuracy INT,
        device TEXT,
        motion TEXT
        );
    """

    sql_create_path_min_table = """CREATE TABLE IF NOT EXISTS path_min (
        LONG FLOAT,
        LAT FLOAT,
        ALT INT,
        speed INT,
        timestamp DATETIME,
        horizontal_accuracy INT,
        vertical_accuracy INT,
        device TEXT,
        motion TEXT
        );
    """

    sql_create_visits_table = """CREATE TABLE IF NOT EXISTS visits (
        LONG FLOAT,
        LAT FLOAT,
        arrival DATETIME,
        departure DATETIME,
        device TEXT
        );
    """

    # create a database connection
    conn = create_connection(database_path)

    # create tables
    if conn is not None:
        # If database does not exist, create tables
        create_table(conn, sql_create_raw_table)
        create_table(conn, sql_create_path_table)
        create_table(conn, sql_create_path_min_table)
        create_table(conn, sql_create_visits_table)
    else:
        print("Error! Cannot create the database connection.")
    
    return conn


if __name__ == '__main__':
    main('daniel')