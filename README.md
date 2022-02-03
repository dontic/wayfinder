# wayfinder

> :warning: Under early developement

## What is wayfinder?
Wayfinder is a server application that reads, process, stores and displays data gathered by the overland-ioss app.

Wayfinder is built in Python with it's main libraries being Pandas for data processing and Plotly for the display maps.

## Usage

For example purposes it's going to be assumed that the server is going to be set up on a debian environment like Raspbian.

You will also need to have ```python3``` installed.

> :information_source: [Click here]() for a tutorial on how to set up Raspbian on your Raspberry Pi.

### 1. Clone the repository

In this example de installation directory is going to be the home directory of the user.

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

You will also need to create the `database` directory. This is where the users' databases will be stored.

```bash
mkdir database
```

It's good practice to periodically back-up this `database` directory somewhere safe. Otherwise, if something goes wrong, you risk loosing all the data stored there.

### 2. Initialize the app

There are several ways you can do this:

#### 2.1 The easiest way

Just run the app directly on your server.

Install the dependencies first:
```bash
pip install -r requirements.txt
```

```bash
python3 app.py
```

This will initiallize the app in your server on port 5012 by default. You can modify this port in `app.py`

>:warning: Note that if the server goes down or something crashes, you will need to manually restart the app each time.

#### 2.2 The resilent way

`supervisor` is a great way to run and monitor your app in the background so you can user your server for more things.

There are also other methods, like `cron`.

A really good supervisor guide [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps).

### 3. Set the credentials

The server app is set-up with basic authentication, so that only the users you allow can upload data to the server.

This is done in 2 steps:

**3.1 Set user credentials in users.json**

Go to the repo in your server and edit the ```users.json``` file with your desired user and passwords combinations.

```bash
cd /home/user/wayfinder
```

```bash
nano users.json
```
You will then see these contents:
```bash
{
    "user": "password",
    "other_user": "other_pw"
}
```
Edit the json file as needed and save it by pressing ```ctrl+x``` and then ```enter```.

**3.2 Overland App setup**

In the Overland App on your phone, go to settings and setup the Receiver Endpoint to point to your server's API:

```
http://yourPublicIP:port/api/?user=<your_user>&pwd=<your_password>
```

Replace ```<your_user>``` and ```<your_password>``` with the user and password you have previously set in users.json

> :warning: The password specified here is not safe in any way, think of it more as a token. DO NOT use a password from another service here!

> :information_source: Check the [Overland Repo]() for detailed information on how to set up the Overland App in your phone
