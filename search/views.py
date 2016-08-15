#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from math import sqrt

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from simplekml import Kml, AltitudeMode, GxAltitudeMode

from search.models import *
from ibri.settings import *
from utils.aes import AESCipher, JavaAESCipher
from utils.tsp import *

import codecs
import sys
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

@login_required(login_url='login/')
def searchMap(request):
    clients = Clients.objects.filter(insearch=True)

    drones = Drone.objects.all()
    return render(request, 'gsoc.html', {
        'client': clients,
        'WEATHER_API': settings.WMAPAPI,
        'KMLDir': settings.KML_DIR,
        'DRONES': drones,
        'nodrones': len(drones)
    })

def resumeMission(request, pk):

    mission = get_object_or_404(Mission, pk=pk)
    j = []
    for m in mission.inSearch.all():
        j.append(str(m.id))

    routes = Route.objects.filter(mission=mission)

    print routes[0]

    return render(request, 'pages/resume.html', {
        'mission': mission,
        'based': routes[0],
        'section': 'Resume Mission',
        'insearch': mission.inSearch.all(),
        'selected': ','.join(j),
        'GAPI': settings.GAPI
    } )

def getTracking(request):

    if (request.method == 'POST'):
        missionId = Mission.objects.get(pk=request.POST['mId'])
        routes = Route.objects.filter(mission=missionId)

        beacons = []
        for user in missionId.inSearch.all():
            beacons.append(user.id)

        print("[i] Beacons in search "+str(beacons))

        droneTracking = [[] for _ in range(len(routes))]

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

        preshared = b'preshared_key012'
        return HttpResponse(AESCipher(preshared).encrypt(json.dumps((droneTracking))))

    else:
        return Http404()

@csrf_exempt
def setTracking(request):

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

    if(request.method == 'GET'):

        droneId = int(droneId)

        M = Mission.objects.last()
        routes = Route.objects.filter(mission=M)
        wp = WayPoint.objects.filter(route=routes[droneId-1])
        missionId = M.pk

        insearch = []
        positions = []

        M = M.inSearch.all()

        for p in M:
            insearch.append(json.dumps({'physicalCode': p.physicalCode}))

        for p in wp:
            positions.append(json.dumps({'lat': p.lat, 'lng': p.lng}))

        return HttpResponse(JavaAESCipher(settings.SKEY).encrypt(json.dumps({'mid': missionId, 'insearch': insearch, 'positions': positions})))


    else:
        raise Http404("Error")

@csrf_exempt
def setDroneTracking(request):

    if(request.method == 'POST'):

        d = json.loads(JavaAESCipher(settings.SKEY).decrypt(request.POST['info']))
        print colored('+ Received From Drone: '+str(d)[0:100], 'blue')

        if d['missionId'] <= 0:
            print colored('+ Error receiving drone information', 'red')
            return HttpResponse("SystemFail")

        m = Mission.objects.get(pk=d['missionId'])
        r = Route.objects.filter(mission=m)
        w = WayPoint.objects.filter(route=r[d['droneId']-1])

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

                wp = WayPoint(route=Route.objects.get(pk=r[d['droneId']-1].id),
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

    if(request.method == 'POST'):

        dec = json.loads(AESCipher(b'preshared_key012').decrypt(request.POST['msg']))

        base = json.loads(dec['base'])
        coords = json.loads(dec['wayPoints'])
        nearPoint = json.loads(dec['nearPoint'])
        userPK = json.loads(dec['insearch'])
        altitude = json.loads(dec['altitude'])


        nAreas = len(coords)
        totalElements = 0
        for i in coords:
            totalElements += len(i)

        size = int(sqrt(totalElements))
        nElements = int(math.floor(math.sqrt(len(coords[0]))))

        searchArea = [[[] for _ in range(nElements)] for _ in range(nAreas)]

        ov1 = 0
        ov2 = 0

        for i in range(nAreas):
            for j in range(nElements):

                col = j * size

                if(ov1 == 0):
                    searchArea[i][j] = coords[i][(col-ov2):(col-ov2)+size]
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

        for i in range(nAreas):
            coord.append([])
            for j in searchArea[i]:
                for k in j:
                    coord[i].append([(x / size), (x % size)])
                    x += 1

        ac = 0
        route = []

        for i in range(nAreas):

            n, D = mk_matrix(coord[i], distL2)
            tour = nearest_neighbor(n, (((nearPoint[i][0] * size)-ac) + nearPoint[i][1]), D)

            for j in range(len(tour)):

                tmpValue = tour[j] + (size - len(searchArea[i][0]))
                col = tmpValue / size

                if col == 0 and i > 0:
                    row = (tmpValue % size) - (size - len(searchArea[i][0]))
                    print(str(tour[j]) + " = " + str(col) + "," + str((tmpValue % size) - (size - len(searchArea[i][0]))))
                else:
                    row = tmpValue % size
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
            print("\033[91m Oops!  No drones found un database")
            return HttpResponse('configerror')

        colorArray =  [
            'ff00008b', #darkred
            'ff8b0000', #darkblue
            'ff006400', #darkgreen
            'ff008cff', #darkorange
            'ff9314ff', #darkpink
            'ffff0000', #blue
            'ff2fffad', #greenyellow
            'ff5c5ccd', #indianred
            'ffcbc0ff', #pink
            'ffe16941', #royalblue
            'ff00ffff', #yellow
        ];


        drone_secuencial = 0
        from os import mkdir
        for r in route:

            rm = Route(mission=m, drone=Drone.objects.all()[drone_secuencial], baseLat=base[0], baseLng=base[1], initialWp=0)
            rm.save()
            tmpRoute = []
            tmpCounter = 0

            kmlName = 'IBRI'+str(m.id)+'R'+str(rm.id)
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

            place = settings.KML_DIR + '/IBRI' + str(m.id)
            place.replace('//', '/')


            try:
                os.mkdir(place)
            except:
                pass

            kml.save(place + '/' + kmlName + '.kml')  # Saving

            drone_secuencial += 1

        preshared = b'preshared_key012'
        return HttpResponse(AESCipher(preshared).encrypt(json.dumps([m.pk, route])))

