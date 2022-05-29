
#!/bin/bash
# Sets up necessary dependencies and systems for Wayfinder
# Script must be executed directly from the package path
# Script needs root permissions

# Install required packages
echo "Installing required packages..."
apt install supervisor python3-pip python3-venv

# Create venv
echo "Createing virtual environment..."
python3 -m venv venv

# Activate venv
echo "Activating virtual environment..."
. venv/bin/activate

# Install package requirements
echo "Installing required packages..."
pip install -r ./requirements.txt

# Install gunicorn
echo "Installing gunicorn..."
pip install gunicorn

# Deactivate env
echo "Deactivating virtual environment..."
deactivate

# Create gunicornlog directories
echo "Creating log directory..."
mkdir logs

# Set up supervisor conf
echo "Creating supervisor conf file..."
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
echo "Reloading supervisor..."
supervisorctl reread
service supervisor restart