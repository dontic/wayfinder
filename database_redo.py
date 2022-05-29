import sqlite3
from pathlib import Path
from app.auth.signup import create_user_location_database
from app.api import sql_connection
from app.api.data_processor import raw_sql_dump, visits, checkins, path_sql_dump
from app.auth.models import User
import pandas as pd

user = User(name='Daniel', username='daniel')

# Read old database
old_db = Path.cwd() / 'database' / ('%s_old.db' % user.username)
con_old = sqlite3.connect(old_db)
query = "SELECT * from raw"
df = pd.read_sql_query(query, con_old)

df = df.drop_duplicates()
df['properties_timestamp'] = pd.to_datetime(df['properties_timestamp'])
df['properties_arrival_date'] = pd.to_datetime(df['properties_arrival_date'])
df['properties_departure_date'] = pd.to_datetime(df['properties_departure_date'])

create_user_location_database(user)

conn = sql_connection.create_connection(user)

raw_sql_dump(df, conn)

df_visits = visits(df, conn)
print(df_visits)

last_checkin = checkins(df, user)

df_path = path_sql_dump(df, conn, df_visits, last_checkin)
