Welcome to IBRI! (GSoC 16)
===================

This project is proposing of a civil security solution using physical web as main technology and drones (UAV) to find missing people. The way to find them is by using multiple unattended aerial vehicles (as known as drone). The main idea from this project is to find a missing person scanning an area with one or more drones who will be receiving the physical web beacon Bluetooth signal to determinate the gps position from it in case of emergency.

----------

Prerequisites
----------

Install keyczar: https://pypi.python.org/pypi/python-keyczar
Install virtualenv: https://virtualenv.pypa.io/en/stable/
Install python

Getting Started
-------------

> **Copy and paste in a console/terminal:**
> git clone git@github.com:LiquidGalaxyLAB/IBRI.git
> cd IBRI/
> virtualenv ENV
> source ENV/bin/activate
> pip install -r requirements.txt
> echo 'DEBUG = True' >> local_settings.py
> mkdir fieldkeys
> keyczart create --location=fieldkeys/ --purpose=crypt
> ./manage.py makemigrations
> ./manage.py migrate
> ./manage createsuperuser # follow the prompt instruction
> ./manage.py runserver

Now open http://localhost:8000/admin/ and login in the system. Then, create some clients and drones. As preshared_key in drones insert ``clave_droneX'' where X is the drone id in the same order as creating (1, 2, 3..). 