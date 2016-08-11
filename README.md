Google Summer of Code 2016

Project IBRI

Project IBRI Drone

Student Moisés Lodeiro Santiago

Developed under GSoC 2016 project Physical Web Project

Welcome to IBRI Project
=======================

This project is proposing of a civil security solution using physical web as main technology and drones (UAV) to find missing people. The way to find them is by using multiple unattended aerial vehicles (as known as drone). The main idea from this project is to find a missing person scanning an area with one or more drones who will be receiving the physical web beacon Bluetooth signal to determinate the gps position from it in case of emergency.


Prerequisites
-------------

- [DJango](https://www.djangoproject.com)


###1. Install packages:
```
apt-get install git virtualenvwrapper python-virtualenv python-dev gcc -y
```

###2. Get the latest git version and go inside:
```
git clone https://github.com/LiquidGalaxyLAB/IBRI.git
```

###3. Create environment and install dependencies:
```
chmod 777 IBRI # only if you have database writting problems
cd IBRI
virtualenv env
source env/bin/activate
pip install -r requeriments.txt
```

###4. Export local settings variables

Get maps api key from [Google developers](https://developers.google.com/)
Get weather api key from [Openweathermap](http://openweathermap.org/)

```
python installer.py # and follow the instructions
```

or

```
echo 'WMAPAPI = "<API_KEY>"' >> local_settings.py
echo 'GAPI = "<API_KEY>"' >> local_settings.py
echo 'IBRI_URL = "https://www.your.url/ibri_path/"' >> local_settings.py
echo 'KML_DIR = "/path/to/save/kml/files/"' >> local_settings.py
chmod 777 db.sqlite3
```

By default the project contains a pair of keys to sign inside fieldkeys dir. If you want to create your own pair run this (warning, if you change the keys the default db.sqlite3 won't work):

```
keyczart create --location=fieldkeys/ --purpose=crypt
keyczart addkey --location=fieldkeys/ --status=primary
```

###5. Run server
```
ibri-start <ip> <port>
```

Or

```
source env/bin/activate # if not activated
python manage.py migrate # optional
python manage.py runserver <ibri_ip> <ibri_port> # optional arguments
```

###+ Linked projects
- [IBRI Drone](https://github.com/LiquidGalaxyLAB/IBRI_Drone/)