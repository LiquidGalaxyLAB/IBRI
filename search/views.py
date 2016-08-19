#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Search views contains all the functions that are necesary to use in the
search application.
@author: Moises Lodeiro-Santiaog
"""

# Python imports
import json
import codecs
import sys
from math import sqrt

# Django imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from simplekml import Kml, AltitudeMode, GxAltitudeMode

# Own imports
from search.models import *
from ibri.settings import *
from utils.aes import AESCipher, JavaAESCipher
from utils.tsp import *

# Set the output as UTF-8 format
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# ---------------------------------------------------------------------

@login_required(login_url='login/')
def searchMap(request):
    """
    The searchMap function takes the clients list that are marked as
    'inSearch', also takes the drone list and the configuration vars
    like WEATHER_API, KMLDir to render the gsoc.html (operator panel)
    Html.

    @param request: Request petition that is handled by Django
    @return: Http response
    @note: This functions requires a previous login
    @precondition: User loged
    @see: django.contrib.auth.decorators.login_required
    """

    clients = Clients.objects.filter(insearch=True) # Clients in search
    drones = Drone.objects.all() # All drones

    return render(request, 'gsoc.html', {
        'client': clients,
        'WEATHER_API': settings.WMAPAPI,
        'KMLDir': settings.KML_DIR,
        'GAPI': settings.GAPI,
        'DRONES': drones,
        'nodrones': len(drones)
    })


def resumeMission(request, pk):
    """
    Resume Mission is called when the opeartor loses the connection
    with the main operator panel. Also, to render the HTML is needed
    the Google API identifier to load the google map.

    @param request: Request petition that is handled by Django
    @param pk: Mission identifier. Is stablished using the public key of the model
    @type pk: C{int}
    @precondition: User loged
    @see: Route
    @return: Http response

    Example:
        - url: /admin/mission/resume/5/ to resume the mission number 5 (mambo!)

    """

    mission = get_object_or_404(Mission, pk=pk) # Get the mission or 404
    j = []

    # Create user insearch identifier list  
    for m in mission.inSearch.all():
        j.append(str(m.id))

    routes = Route.objects.filter(mission=mission)

    return render(request, 'pages/resume.html', {
        'mission': mission,
        'based': routes[0],
        'section': 'Resume Mission',
        'insearch': mission.inSearch.all(),
        'selected': ','.join(j),
        'GAPI': settings.GAPI
    })


def getTracking(request):
    """
    Get Tracking returns the drone tracking information to the operator
    panel. When the HTML panel requires the drone tracking this method
    is called. 
    
    @param request: Request petition that is handled by Django
    @precondition: User loged
    @return: Http response (JSON)
    @see: HttpResponse
    @see: AESCipher
    @see: JSON
    @note: See the source code to get more information about how this
           function works.
    """

    # Only allows POST request
    if (request.method == 'POST'):

        # Get mission filtered by request mission id
        missionId = Mission.objects.get(pk=request.POST['mId'])
        # Get routes contained in that mission
        routes = Route.objects.filter(mission=missionId)
        # Create a list of user identifications that are in search
        beacons = []
        for user in missionId.inSearch.all():
            beacons.append(user.id)

        if DEBUG:
            print("[i] Beacons in search " + str(beacons))

        # Create a empty list. Each position correspond to each route
        # id.
        droneTracking = [[] for _ in range(len(routes))]

        """
        In this 'for' we take the waypoints that contains the route 'rid'
        and filtered by the waypoint.visited. Then, if theres no waypoints
        that are visited we include in the droneTracking list an empty
        reference the temp latitude and longitude and no photo.
        If wp contains any data we check if any waypoint has a physical
        web beacon signal we include that signal in the droneTracking
        list. If the drone send any photo we also include it in the
        request.
        """

        i = 0
        for rid in routes:

            waypoints = WayPoint.objects.filter(route=rid).order_by('updated')
            waypoints = filter(lambda w: w.visited is True, waypoints)

            if waypoints == []:
                droneTracking[i].append(["", rid.tmpLat, rid.tmpLng, None, None, None, rid.tmpLat, rid.tmpLng])

            for wp in waypoints:

                if wp.signalFound in beacons:
                    u = missionId.inSearch.get(pk=wp.signalFound)
                    print(u"[ Beacon found ] - {} {} - {} - {}".format(u.name, u.lastname, u.identifier, u.physicalCode))
                    print(u"[#{} - {}, {}]".format(wp.ref, wp.lat, wp.lng))

                if wp.photo:
                    droneTracking[i].append([wp.ref, wp.lat, wp.lng, wp.visited, wp.signalFound, wp.photo, rid.tmpLat, rid.tmpLng])
                else:
                    droneTracking[i].append([wp.ref, wp.lat, wp.lng, wp.visited, wp.signalFound, "", rid.tmpLat, rid.tmpLng])

            i += 1

        preshared = u''+settings.PRESHAREDKEY
        return HttpResponse(AESCipher(preshared).encrypt(json.dumps((droneTracking))))

    else:
        return Http404()


@csrf_exempt
def setTracking(request):
    """
    Set Tracking allows to simulate a drone in combination with the
    management command.

    @param request: Request petition that is handled by Django
    @type request: Django request object
    @deprecated: This function was used when we don't have any real drone
    application.
    """

    if (request.method == 'POST'):

        droneKey = Drone.objects.get(pk=int(request.POST['droneId']))
        d = json.loads(AESCipher(droneKey.preSharedKey.ljust(32)[:32]).decrypt(request.POST['info']))
        wp = WayPoint.objects.get(pk=int(d['id']))

        if d['scan'] != None:
            wp.signalFound = int(d['scan'])
            print("[ Beacon Found ] - Checking #" + str(d['scan']))

        wp.visited = True
        wp.photo = d['photo']
        wp.save()
        return HttpResponse("Visited "+str(wp))

    else:
        raise Http404("Error")


@csrf_exempt
def getDroneMissionData(request, droneId):
    """
    Get Drone Mission Data is a function that is used to return to the
    drone the mission data. This method don't requires a CSRF token.

    @param request: Request petition that is handled by Django
    @type request: Django request object
    @param droneId: Drone identification. Each drone is linked to each route
    @type droneId: int
    @return: Http response (JSON)
    @see: HttpResponse
    @see: AESCipher
    @see: JSON
    @see: csrf_extemp
    """

    if(request.method == 'GET'):

        droneId = int(droneId)
        M = Mission.objects.last() # The drone will receive the last mission information
        routes = Route.objects.filter(mission=M) # Routes in that mission
        wp = WayPoint.objects.filter(route=routes[droneId-1]) # Waypoints for those routes
        missionId = M.pk
        insearch = []
        positions = []

        M = M.inSearch.all() # Identifier for each user that is in search

        for p in M:
            insearch.append(json.dumps({'physicalCode': p.physicalCode}))

        for p in wp:
            positions.append(json.dumps({'lat': p.lat, 'lng': p.lng}))

        return HttpResponse(JavaAESCipher(settings.SKEY).encrypt(json.dumps({'mid': missionId, 'insearch': insearch, 'positions': positions})))

    else:
        raise Http404("Error")


@csrf_exempt
def setDroneTracking(request):
    """
    Set Drone Tracking is the method that a drone uses to inform to the server
    of it position sending via POST the encrypted information. This method don't
    use the CSRF token.

    @param request: Request petition that is handled by Django
    @type request: Django request object
    @return: Http response (JSON)
    @see: HttpResponse
    @see: AESCipher
    @see: JSON
    @see: csrf_extemp
    """

    if(request.method == 'POST'):

        # Decoded data. This variable stores the unencrypted value of a JSON
        # string loaded in POST['info'].
        d = json.loads(JavaAESCipher(settings.SKEY).decrypt(request.POST['info']))

        if DEBUG:
            print colored('+ Received From Drone: '+str(d)[0:100], 'blue')

        if d['missionId'] <= 0:
            print colored('+ Error receiving drone information', 'red')
            return HttpResponse("SystemFail")

        m = Mission.objects.get(pk=d['missionId'])
        r = Route.objects.filter(mission=m)
        w = WayPoint.objects.filter(route=r[d['droneId'] - 1])

        """
        This conditional checks if the sended data from the drone contains
        the nearpoint value. This represents that if the drone is near a
        waypoint (<10m) the waypoint that will be taken is that one. If not,
        in the else condition we create a new waypoint and fill the data that
        corresponds to it.
        Also, in both of cases we check if the drone sends a photo and if that,
        we store it in base64 format in the waypoint.
        """

        if d['nearpoint'] >= 0 and d['nearpoint'] < r[d['droneId']-1].initialWp:

            w = w.get(ref=d['nearpoint'])
            w.visited = True

            print colored(str(w), 'red')

            if d['photo'] != "":

                if w.photo != "":
                    w.photo = d['photo']
                    w.save()
                    print colored('WayPoint object has been updated', 'green')
                else:
                    c = Clients.objects.get(physicalCode=d['beacon'])
                    wp = WayPoint(route=Route.objects.get(pk=r[d['droneId']-1].id),
                              ref=(w.last().ref+1),
                              lat=d['latitude'],
                              lng=d['longitude'],
                              visited=True,
                              signalFound=c.pk,
                              photo=d['photo'])
                    wp.save()

            if d['beacon'] != "":
                c = Clients.objects.get(physicalCode=d['beacon'])
                w.signalFound = c.pk
                w.save()

        else:

            if d['photo'] != '' or d['beacon'] != '':

                c = Clients.objects.get(physicalCode=d['beacon'])

                wp = WayPoint(route=Route.objects.get(pk=r[d['droneId'] - 1].id),
                              ref=(w.last().ref+1),
                              lat=d['latitude'],
                              lng=d['longitude'],
                              visited=True,
                              signalFound=c.pk,
                              photo=d['photo'])
                wp.save()

            else:
                rid = Route.objects.get(pk=r[d['droneId']-1].id)
                rid.tmpLat = d['latitude']
                rid.tmpLng = d['longitude']
                rid.save()

        return HttpResponse("OK")


def createRoute(request):
    """
    Create Route is one of the main methods in the software because it
    creates the routes for each drone in the mission. It takes
    the POST['msg'] information. Then gets the square waypoints grid
    and divides it in many areas as drones we have. This method is
    triggered when the operator clicks on the play button.

    The areas are created and stored in the database and whe it's done
    we create a KML file/s and stores it in the KML_DIR path under the
    IBRI folder.

    @param request: Request petition that is handled by Django
    @type request: Django request object
    @return: Http response (JSON)
    @requires: utils.tsp
    @see: HttpResponse
    @see: AESCipher
    @see: JSON
    @see: csrf_extemp
    @see: WayPoint
    @see: Route
    @see: KML
    @see: utils.tsp.py
    @note: If you want to see how createRoute works, click on see source code.
    """

    if(request.method == 'POST'):

        # Get the preshared key and decrypt the post message.
        preshared = u'' + PRESHAREDKEY
        dec = json.loads(AESCipher(preshared).decrypt(request.POST['msg']))

        # Loads the json and stores the values in each variable
        base = json.loads(dec['base'])  # Base point
        coords = json.loads(dec['wayPoints'])  # Waypoints (lat, lng)
        nearPoint = json.loads(dec['nearPoint'])  # NearPoint
        userPK = json.loads(dec['insearch'])  # Users in search
        altitude = json.loads(dec['altitude'])  # Altitude

        # Number of areas
        nAreas = len(coords)
        totalElements = 0
        for i in coords:
            totalElements += len(i)

        size = int(sqrt(totalElements))
        nElements = int(math.floor(math.sqrt(len(coords[0]))))

        searchArea = [[[] for _ in range(nElements)] for _ in range(nAreas)]

        ov1 = 0
        ov2 = 0

        # Area divison
        for i in range(nAreas):

            for j in range(nElements):
                col = j * size

                if(ov1 == 0):
                    searchArea[i][j] = coords[i][(col-ov2):(col-ov2) + size]
                else:
                    searchArea[i][j] = coords[i][0:ov1]
                    ov2 = size - ov1
                    ov1 = 0

            if(len(searchArea[i][j]) == 0):
                searchArea[i].pop()
                j -= 1

            if(size - len(searchArea[i][j]) > 0):
                ov1 = size - len(searchArea[i][j])
                ov2 = 0
            else:
                ov1 = 0
                ov2 = 0

        coord = []
        x = 0

        # Assign coordenates to each area
        for i in range(nAreas):
            coord.append([])
            for j in searchArea[i]:
                for k in j:
                    coord[i].append([(x / size), (x % size)])
                    x += 1

        ac = 0
        route = []

        # Create an optimal route using the A* algorithm following the TSP
        for i in range(nAreas):

            n, D = mk_matrix(coord[i], distL2)
            tour = nearest_neighbor(n, (((nearPoint[i][0] * size)-ac) + nearPoint[i][1]), D)

            for j in range(len(tour)):

                tmpValue = tour[j] + (size - len(searchArea[i][0]))
                col = tmpValue / size

                if col == 0 and i > 0:
                    row = (tmpValue % size) - (size - len(searchArea[i][0]))
                    if DEBUG:
                        print(str(tour[j]) + " = " + str(col) + "," + str((tmpValue % size) - (size - len(searchArea[i][0]))))
                else:
                    row = tmpValue % size
                    if DEBUG:
                        print(str(tour[j])+" = "+str(col)+","+str(tmpValue % size))

                tour[j] = searchArea[i][col][row]

            ac += len(coord[i])
            route.append(tour)


        m = Mission()
        m.save()

        for userId in range(0, len(userPK)):
            m.inSearch.add(Clients.objects.get(pk=userPK[userId]))

        try:
            drones = Drone.objects.all()[0]
        except:
            print colored("Oops! No drones found un database", 'red')
            return HttpResponse('configerror')

        colorArray = [
            'ff00008b',  # darkred
            'ff8b0000',  # darkblue
            'ff006400',  # darkgreen
            'ff008cff',  # darkorange
            'ff9314ff',  # darkpink
            'ffff0000',  # blue
            'ff2fffad',  # greenyellow
            'ff5c5ccd',  # indianred
            'ffcbc0ff',  # pink
            'ffe16941',  # royalblue
            'ff00ffff',  # yellow
        ]

        drone_secuencial = 0

        # Creates the KML file
        from os import mkdir
        for r in route:

            rm = Route(mission=m, drone=Drone.objects.all()[drone_secuencial], baseLat=base[0], baseLng=base[1], initialWp=0)
            rm.save()
            tmpRoute = []
            tmpCounter = 0

            kmlName = 'IBRI' + str(m.id) + 'R' + str(rm.id)
            kml = Kml(name=kmlName)

            kml.newpoint(name="Base", coords=[(base[1], base[0])])

            pnt = kml.newlinestring(name='Route {}'.format(tmpCounter))
            coords = []

            for wp in r:
                coords.append((wp[1], wp[0], altitude))
                tmpRoute.append(WayPoint(route=rm, lat=wp[0], lng=wp[1], ref=tmpCounter))
                tmpCounter += 1

            pnt.coords = coords
            pnt.style.linestyle.width = 6
            pnt.style.linestyle.color = colorArray[drone_secuencial % len(colorArray)]

            pnt.altitudemode = AltitudeMode.relativetoground
            pnt.lookat.gxaltitudemode = GxAltitudeMode.relativetoseafloor
            pnt.lookat.latitude = coords[0][0]
            pnt.lookat.longitude = coords[0][1]
            pnt.lookat.range = 122
            pnt.lookat.heading = 0.063
            pnt.lookat.tilt = 0

            tmpRoute.append(WayPoint(route=rm, lat=base[0], lng=base[1], ref=tmpCounter))
            kml.newpoint(name="Back to base", coords=[(base[1], base[0])])

            rm.initialWp = len(tmpRoute)-2 # -2 for the last tmp counter and array 0 position
            rm.save()

            WayPoint.objects.bulk_create(tmpRoute)

            place = KML_DIR + '/IBRI' + str(m.id)

            try:
                mkdir(place)
            except Exception as e:
                print colored(e, 'red')
                pass

            place = place + '/' + kmlName + '.kml'
            place.replace('//', '/')

            try:
                kml.save(place)  # Saving
            except Exception as e:
                print colored(e, 'red')
                return HttpResponse('errorKmlPath')

            drone_secuencial += 1

        preshared = u'' + PRESHAREDKEY
        return HttpResponse(AESCipher(preshared).encrypt(json.dumps([m.pk, route])))
