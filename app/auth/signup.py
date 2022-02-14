from flask import redirect, url_for, flash
from flask_login import login_user
from app.auth.models import User
from app.extensions import db
from pathlib import Path
from app.api.sql_connection import create_connection, create_table
from werkzeug.security import generate_password_hash, check_password_hash


def create_user_location_database(user):

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
        device TEXT,
        duration FLOAT
        );
    """

    conn = create_connection(user)

    # If database does not exist, create tables
    create_table(conn, sql_create_raw_table)
    create_table(conn, sql_create_path_table)
    create_table(conn, sql_create_path_min_table)
    create_table(conn, sql_create_visits_table)

    return True


def process_user(request):
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    apikey = request.form.get('apikey')

    user_email = User.query.filter_by(email=email).first()
    if user_email:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    user_username = User.query.filter_by(username=username).first()
    if user_username:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    # Add new user to the sqlite database
    new_user = User(name=name, email=email, username=username, password=generate_password_hash(password, method='sha256'), apikey=generate_password_hash(apikey, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    # Create user's location database
    create_user_location_database(new_user)

    # Sign in the user automatically
    login_user(new_user, remember=False)
    return redirect(url_for('site.overview'))


if __name__ == '__main__':
    pass