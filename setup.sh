
#!/bin/bash
# Sets up necessary dependencies and systems for Wayfinder
# Script must be executed directly from the package path
# Script needs root permissions

# Install required packages
apt install supervisor python-pip python-virtualenv

# Create venv
echo "Createing virtual environment..."
python3 -m venv venv

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Install package requirements
echo "Installing required packages..."
pip install -r ./requirements.txt

# Install gunicorn
echo "Installing gunicorn..."
pip install gunicorn

# Create user database

# Deactivate env
echo "Deactivating virtual environment..."
deactivate

# Create gunicornlog directories
mkdir logs

# Set up supervisor conf
cat > /etc/supervisor/conf.d/wayfinder.conf << EOF

[program:wayfinder]
directory = /home/$USER/wayfinder
command = /home/$USER/wayfinder/venv/bin/gunicorn -b 0.0.0.0:5012 --timeout 300 run:app
stdout_logfile = /home/$USER/wayfinder/logs/gunicorn.stdout.log
stderr_logfile = /home/$USER/wayfinder/logs/gunicorn.stderr.log
logfile_backups=2
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8 ; Set UTF-8 as default encoding
autostart=true
autorestart=true
startsecs=0
stopwaitsecs=600
EOF

# Reload supervisor
supervisorctl reread
service supervisor restart