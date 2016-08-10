# -*- coding: utf-8 -*-
import os

template = """#IBRI Local Config
LANGUAGE_CODE = '{}'
DEBUG = {}
KML_DIR = '{}'
GAPI = '{}'
WMAPAPI = '{}'
{}
IBRI_URL = '{}'
"""

confirm = False

if not os.path.exists('fieldkeys'):
    os.makedirs('fieldkeys')

while confirm == False:

	print 'IBRI Installer'
	print '--------------\n'

	if raw_input('> Change default en-EN langauge? (y/n): ') in 'y':
		language_code = raw_input('Language? Default: en-EN: ')
	else:
		language_code = 'en-EN'

	if raw_input('> Enable debug mode? (y/n): ') in 'y':
		debugi = 'True'
	else:
		debugi = 'False'
	
	kml = raw_input('> Where will be saved the kml files?: ')
	if not kml.endswith('/'):
		kml += '/'

	try:
		os.chmod(kml, 0o777)
	finally:
		pass

	if not os.path.exists(kml):
		os.makedirs(kml)

	gapi = raw_input('> Insert your Google API to use the Google Services (like google maps): ')
	
	wmap = raw_input('> Insert your OpenWeatherMap Api Key: ')
	
	skey = ''
	if raw_input('> Change default secret key? (y/n): ') in 'y':
		while len(skey) != 14:
			skey = raw_input('> Insert your secret key used in communications (14 chars length). Example LHnhUqmgS1KWh4: ')
		skey = 'SKEY = "'+skey+'"'
	else:
		skey = 'SKEY = "QHahUjmgS7KWh3"'

	url = ''
	print '> What is the IBRI url? (https and ends with slash) \n'
	print 'Example: https://www.your.url./ibri/'
	while not url.startswith('https') or not url.endswith('/'):
		url = raw_input('> Url: ')
	
	temp = template.format(language_code, debugi, kml, gapi, wmap, skey, url)
	print "\n"*3
	print temp

	confirm = raw_input('Save the configuration file in local_settings.py? [y/n]: ')
	if confirm == 'y':
		f = open('local_settings.py', 'w+')
		f.write(temp)
		f.close()

	try:
		os.chmod('db.sqlite3', 0o777)
	except:
		print 'Cannot change chmod 777 to db.sqlite3'