#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contain the function to create shortened URL using Google Shortener
"""

# Metadata
__author__ = 'Moises Lodeiro Santiago'
__credits__ = ['Moises Lodeiro-Santiago']
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = 'Moises Lodeiro-Santiago'
__email__ = "moises.lodeiro[at]gmail.com"
__status__ = "Production"

# Python Imports
import json
import requests

# Third party imports
from requests import ConnectionError

# Own imports
from ibri import settings


def short_url(url):
    """
    Short Url receives a long url and then connects to the Google Shortener
    service to get a shorted URL.

    @param url: String with a long url
    @returns: Shorted url if not exeption raises
    @raises ConnectionError: Raises when the application cannot connect to Google
    @raises KeyError: If the response hasn't got the id field, returns KeyError
    """

    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key='+settings.GAPI
    params = json.dumps({'longUrl': url})

    try:
    	response = requests.post(post_url, params, headers={'Content-Type': 'application/json'})
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