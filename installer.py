# -*- coding: utf-8 -*-

template = """#IBRI Local Config
STATIC_ROOT = '{}'
STATIC_URL = '{}'
LANGUAGE_CODE = '{}'
DEBUG = {}
KML_DIR = '{}'
KML_ICON = 'https://i.imgsafe.org/9216fc4611.png'
GAPI = '{}'
WMAPAPI = '{}'
SKEY = '{}'
IBRI_URL = '{}'
"""

confirm = False

while confirm == False:

	print 'IBRI Installer'
	print '--------------\n'
	static_root = raw_input('Enter the full path of the IBRI directory: ')
	
	if not static_root.endswith('/'):
		static_root += '/'

	static_url = raw_input('Where will be the static folder inside the project?: ')
	if not static_url.endswith('/'):
		static_url += '/'

	language_code = raw_input('Language? Default: en-EN: ')

	debugi = ''
	while debugi not in {'True', 'False'}:
		debugi = raw_input('Debug? (True or False): ')
	
	
	kml = raw_input('Where will be saved the kml files? directory must have write permissions: ')
	if not kml.endswith('/'):
		kml += '/'

	gapi = raw_input('Insert your Google API to use the Google Services (like google maps): ')
	

	wmap = raw_input('Insert your OpenWeatherMap Api Key: ')
	
	skey = ''
	while len(skey) != 14:
		skey = raw_input('Insert your secret key used in communications (14 chars length). Example LHnhUqmgS1KWh4: ')

	url = ''
	while not url.startswith('https'):
		url = raw_input('What is the ibri url? (https): ')
	
	temp = template.format(static_root, static_url, language_code, debugi, kml, gapi, wmap, skey, url)
	print temp

	confirm = raw_input('Save the configuration file in local_settings.py? [y/n]: ')
	if confirm == 'y':
		f = open('local_settings.py', 'w+')
		f.write(temp)
		f.close()