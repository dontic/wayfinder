from flask import current_app
import pandas as pd
import sqlite3
import shutil
from datetime import datetime as dt

def delete_duplicates(username):

    pwd = current_app.config['BASE_DIR']
    databasedir = pwd / 'database'

    old_db = databasedir / ('%s.db' % username)
    backup_db = databasedir / ('%s_backup_%s.db' % (username, dt.strftime(dt.now(),'%Y%m%d_%H%M%S')))
    new_db = databasedir / ('%s_new.db' % username)

    con_old = sqlite3.connect(old_db)
    con_new = sqlite3.connect(new_db)

    shutil.copy(old_db, backup_db)

    deldups = 0

    for table in ['raw', 'path', 'visits']:
        query = "SELECT * from %s" % table

        df = pd.read_sql_query(query, con_old)
        old_size = len(df.index)
        print('Current size of %s table : %s' % (table, str(old_size)))

        df = df.drop_duplicates()
        new_size = len(df.index)
        deldups += (old_size - new_size)
        print('Removed %s duplicated rows from %s table.' % (str(old_size - new_size), table))

        df.to_sql(table, con=con_new, index=False)

    old_size = old_db.stat().st_size
    new_size = new_db.stat().st_size

    print('Reduced file size from %s bytes to %s bytes.' % (old_size, new_size))

    print('Deleting old database...')

    shutil.move(new_db, old_db)

    # Remove if more than N_BACKUPS:
    backups = databasedir.glob('%s_backup_*.db' % username)
    if len(backups) > current_app.config['N_BACKUPS']:
        ntoremove = len(backups) - current_app.config['N_BACKUPS']
        filestoremove = backups[:ntoremove]
        for f in filestoremove:
            f.unlink()
        pass

    print('Done.')

    con_old.close()
    con_new.close()

    return deldups, old_size/1000000, new_size/1000000


if __name__ == '__main__':
    delete_duplicates(input('Username: '))