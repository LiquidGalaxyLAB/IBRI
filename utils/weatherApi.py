#coding -*- utf-8 -*-
import json
import requests
from django.http import HttpResponse

from ibri import settings


def getWeather(request, lat, lng):

    if (request.method == 'POST'):
        url = 'http://api.openweathermap.org/data/2.5/weather';
        r = requests.get(url+"?units=metric&lat="+lat+"&lon="+lng+"&appid="+settings.WMAPAPI)
        return HttpResponse(r.text)


