#coding -*- utf-8 -*-
import json
import requests
from ibri import settings

def short_url(url):

    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key='+settings.GAPI
    params = json.dumps({'longUrl': url})
    response = requests.post(post_url,params,headers={'Content-Type': 'application/json'})
    return response.json()['id']
