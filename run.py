import pwd
from app import create_app
app = create_app()

# Create SQLITE3 users database if it doesn't exist
from pathlib import Path
if not Path(Path.cwd()/'app'/'users.db').is_file():
    from app.extensions import db
    from app.auth.models import *
    db.create_all(app=app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)