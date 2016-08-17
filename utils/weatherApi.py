#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is a bridge to use HTTPS in local server using HTTP connectin between
the server and the OpenWeatherMap API.
"""

# Metadata
__author__ = 'Moises Lodeiro Santiago'
__credits__ = ['Moises Lodeiro-Santiago']
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = 'Moises Lodeiro-Santiago'
__email__ = "moises.lodeiro[at]gmail.com"
__status__ = "Production"

# Django Imports
import requests
from django.http import HttpResponse

# Own imports
from ibri import settings

def getWeather(request, lat, lng):
    """
    Get Weather receives the latitude and longitude coordinates and makes the
    request petition to the openweathermap api.

    @param lat: Latitude
    @param lng: Longitude
    @require: settings.WMAPAPI
    """

    if (request.method == 'POST'):
        url = 'http://api.openweathermap.org/data/2.5/weather';
        r = requests.get(url+"?units=metric&lat="+lat+"&lon="+lng+"&appid="+settings.WMAPAPI)
        return HttpResponse(r.text)
