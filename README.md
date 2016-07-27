Welcome to IBRI!
===================

This project is proposing of a civil security solution using physical web as main technology and drones (UAV) to find missing people. The way to find them is by using multiple unattended aerial vehicles (as known as drone). The main idea from this project is to find a missing person scanning an area with one or more drones who will be receiving the physical web beacon Bluetooth signal to determinate the gps position from it in case of emergency.

----------

Prerequisites
----------
Login as root in a terminal and execute this:

- apt-get install python-virtualenv -y
- apt-get install git -y
- apt-get install python-dev gcc -y

Getting Started
-------------

**Copy and paste in a console/terminal (no root):**

- cd $HOME # or your workspace
- virtualenv ENV
- source ENV/bin/activate
- pip install -U pip
- git clone https://github.com/LiquidGalaxyLAB/IBRI.git
- cd IBRI
- pip install -r requirements.txt
- echo 'KML_DIR="**directory where kml files will be saved**"' > local_settings.py;
- echo 'DEBUG=True' >> local_settings.py; # For testing purpose
- echo 'WMAPAPI="**insert open weather map api here**"' >> local_settings.py;
- echo 'GAPI="**insert google api here**"' >> local_settings.py;
- echo 'SKEY="**insert secret preshared key here (LHnhUqmgS1KWh4 for example)**" >> local_settings.py'
- echo 'IBRI_URL="http://your.ibri.url/" >> local_settings.py
- mkdir fieldkeys
- keyczart create --location=fieldkeys/ --purpose=crypt
- keyczart addkey --location=fieldkeys/ --status=primary
- ./manage.py makemigrations;
- ./manage.py migrate;

Now the next step is create a super user using:

- ./manage.py createsuperuser # and follow the prompt instructions (your password should be strong)

After creating the administrator account you can open the administration panel (usually located on http://localhost:8000/admin/ ) and login in the system using the superuser account. Then, create some clients and drones. As preshared_key in drones insert ``clave_droneX'' where X is the drone id in the same order as creating (1, 2, 3..). Also, before open the client panel (http://localhost:8000/) you have to insert the **WEATHER_API** in config model (how to obtain weather api http://openweathermap.org/appid#get). 

Linked Project:
https://github.com/moiseslodeiro/IBRI_DRONE/tree/master
