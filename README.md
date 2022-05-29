# wayfinder

## What is wayfinder?
Wayfinder is a Flask application that reads, process, stores and displays data gathered by the overland-ios app.

Wayfinder is built in Python with it's main libraries being Flask for the App (API and data display) and Pandas for data processing.

## Usage

This installation guide is intended for Debian environments.

You will need to have ```python3``` installed.

### 1 Clone the repository

In this example de installation directory is going to be the home directory of ```user```.

```bash
cd /home/user
```
```bash
git clone https://github.com/dontic/wayfinder
```

The folder ```wayfinder``` will be created in that directory with all the necessary code.

```bash
cd wayfinder
```

### 2 Setup Wayfinder

Ensure that ```python3``` is installed in your system.

>```setup.sh``` installs all necessary dependencies and configures supervisor and gunicorn to run Wayfinder. If you preffer to go another route skip this step.


While in the wayfinder directory run the setup script:

```bash
./setup.sh
```


If all goes well the app should be running in 
```
yourServerAdress:5012
```

### 3 Sign up process

Just open any browser and go to the app address:

```
yourServerAdress:5012
```

You will see a Log In and Sign Up tabs at the top.

You can use the Sign Up tab to create your user and API Key.

You can modify your user details in the `settings` tab once you are logged in.

#### 3.1 Enabling and disabling signups

Go to the repo in your server and edit the ```config.py```:

```bash
cd /home/user/wayfinder
nano config.py
# Modify
ENABLE_SIGNUPS = True
# to 
ENABLE_SIGNUPS = False
```

### 4 Overland App setup

In the Overland App on your phone, go to settings and setup the Receiver Endpoint to point to your server's API:

```
http://yourPublicIP:port/api/?username=<your_username>&apikey=<your_api_key>
```

Replace ```<your_username>``` and ```<your_api_key>``` with the user and API Key you have signed up with.

> :information_source: Check the [Overland Repo]() for detailed information on how to set up the Overland App in your phone.