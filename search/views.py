# -*- coding: utf-8 -*-
import json
from math import sqrt

import simplekml
from config.models import Config
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from simplekml import Kml

from search.models import *
from ibri.settings import STATICFILES_DIRS
from utils.aes import AESCipher
from utils.tsp import *


@login_required(login_url='/admin/login/')
def searchMap(request):
    clients = Clients.objects.all()
    weather_api = Config.objects.get(pk='WEATHER_API')
    return render(request, 'gsoc.html', {'client': clients, 'WEATHER_API': weather_api.value, 'KMLDir': settings.KML_DIR})


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

            waypoints = WayPoint.objects.filter(route=rid)
            waypoints = filter(lambda w: w.visited is True, waypoints)

            for wp in waypoints:

                if wp.signalFound in beacons:
                    u = missionId.inSearch.get(pk=wp.signalFound)
                    print(u"[ Beacon found ] - {} {} - {} - {}".format( u.name, u.lastname, u.identifier, u.physicalCode))
                    print("[#{} - {}, {}]".format(wp.ref, wp.lat, wp.lng))

                if wp.photo:
                    droneTracking[i].append([wp.ref, wp.lat, wp.lng, wp.visited, wp.signalFound, wp.photo])
                else:
                    droneTracking[i].append([wp.ref, wp.lat, wp.lng, wp.visited, wp.signalFound])

            print(droneTracking)
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





def createRoute(request):

    if(request.method == 'POST'):

        dec = json.loads(AESCipher(b'preshared_key012').decrypt(request.POST['msg']))

        base = json.loads(dec['base'])
        coords = json.loads(dec['wayPoints'])
        nearPoint = json.loads(dec['nearPoint'])
        userPK = json.loads(dec['insearch'])

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

        #.style.linestyle.width = 5
        #ls.style.linestyle.color = simplekml.Color.blue



        # TODO quitar la variable drone_secuencial
        drone_secuencial = 0
        from os import mkdir
        for r in route:

            # TODO cambiar para que la elección del dron la haga el usuario y no sea secuencial
            rm = Route(mission=m, drone=Drone.objects.all()[drone_secuencial], baseLat=base[0], baseLng=base[1])
            rm.save()
            tmpRoute = []
            tmpCounter = 0

            kmlName = 'IBRI'+str(m.id)+'R'+str(rm.id)
            kml = Kml(name=kmlName)

            kml.newpoint(name="Base", coords=[(base[1], base[0])])

            pnt = kml.newlinestring(name='Route {}'.format(tmpCounter))
            coords = []

            for wp in r:

                coords.append((wp[1], wp[0]))

                #pnt = kml.newpoint(name='Point {}'.format(tmpCounter))
                #pnt.coords = [(wp[1], wp[0])]

                #if settings.KML_ICON != '':
                #    pnt.style.iconstyle.icon.href = settings.KML_ICON

                tmpRoute.append(WayPoint(route=rm, lat=wp[0], lng=wp[1], ref=tmpCounter))
                tmpCounter += 1

            pnt.coords = coords
            pnt.style.linestyle.width = 6
            pnt.style.linestyle.color = colorArray[drone_secuencial % len(colorArray)]

            tmpRoute.append(WayPoint(route=rm, lat=base[0], lng=base[1], ref=tmpCounter))
            kml.newpoint(name="Back to base", coords=[(base[1], base[0])])

            WayPoint.objects.bulk_create(tmpRoute)

            place = settings.KML_DIR + '/IBRI' + str(m.id)

            try:
                os.mkdir(place)
            except:
                pass

            kml.save(place + '/' + kmlName + '.kml')  # Saving

            drone_secuencial += 1

        preshared = b'preshared_key012'
        return HttpResponse(AESCipher(preshared).encrypt(json.dumps([m.pk, route])))



def createRoute_deprecated(request):

    if(request.method == 'POST'):

        dec = json.loads(AESCipher(b'preshared_key012').decrypt(request.POST['msg']))

        base = json.loads(dec['base'])
        coords = json.loads(dec['wayPoints'])
        nearPoint = json.loads(dec['nearPoint'])
        userPK = json.loads(dec['insearch'])

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

        # TODO quitar la variable drone_secuencial
        drone_secuencial = 0
        from os import mkdir
        for r in route:

            # TODO cambiar para que la elección del dron la haga el usuario y no sea secuencial
            rm = Route(mission=m, drone=Drone.objects.all()[drone_secuencial], baseLat=base[0], baseLng=base[1])
            rm.save()
            tmpRoute = []
            tmpCounter = 0

            kmlName = 'IBRI'+str(m.id)+'R'+str(rm.id)
            kml = Kml(name=kmlName)

            kml.newpoint(name="Base", coords=[(base[1], base[0])])

            for wp in r:

                pnt = kml.newpoint(name='Point {}'.format(tmpCounter))
                pnt.coords = [(wp[1], wp[0])]

                if settings.KML_ICON != '':
                    pnt.style.iconstyle.icon.href = settings.KML_ICON

                tmpRoute.append(WayPoint(route=rm, lat=wp[0], lng=wp[1], ref=tmpCounter))
                tmpCounter += 1

            tmpRoute.append(WayPoint(route=rm, lat=base[0], lng=base[1], ref=tmpCounter))
            kml.newpoint(name="Back to base", coords=[(base[1], base[0])])

            WayPoint.objects.bulk_create(tmpRoute)

            place = settings.KML_DIR + '/IBRI' + str(m.id)

            try:
                os.mkdir(place)
            except:
                pass

            kml.save(place + '/' + kmlName + '.kml')  # Saving

            drone_secuencial += 1

        preshared = b'preshared_key012'
        return HttpResponse(AESCipher(preshared).encrypt(json.dumps([m.pk, route])))
