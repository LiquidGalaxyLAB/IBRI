#coding -*- utf-8 -*-
import json
import requests
from requests import ConnectionError
from ibri import settings

def short_url(url):

    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key='+settings.GAPI
    params = json.dumps({'longUrl': url})
    
    try:
    	response = requests.post(post_url,params,headers={'Content-Type': 'application/json'})
    except ConnectionError as e:
    	print 'Request Error: '+str(e)
    	raise

    responseId = ''
    try:
    	print response.json()
    	responseId = response.json()['id']
    	return responseId
    except KeyError:
    	raise