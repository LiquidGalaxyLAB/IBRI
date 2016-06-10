#! /bin/python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# System
import random
import base64
import json
from time import sleep
# -------------------------------------------------------------------
# Django
from django.core.management.base import BaseCommand
from search.models import Route, WayPoint, Mission
from utils.aes import AESCipher
# -------------------------------------------------------------------
# Third party
import requests
# -------------------------------------------------------------------


class Command(BaseCommand):

    @staticmethod
    def take_photo():
        with open("static/img/cenital_photo.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string

    @staticmethod
    def scan():
        beacons = range(1, 10)
        random_value = random.randint(0, 100)

        if random_value < 15:
            return beacons[random.randint(0, 8)]
        return None

    def add_arguments(self, parser):
        parser.add_argument('droneId', nargs='+', type=int)

    def handle(self, *args, **options):
        drone_id = int(options['droneId'][0])
        url_post = 'http://localhost:8000/search/setTracking/'
        shared_key = 'clave_drone' + str(drone_id)  # AES256 pre-shared key with the drone
        shared_key = shared_key.ljust(32)[:32]
        in_search = Mission.objects.last()
        beacons = []

        for user in in_search.inSearch.all():
            beacons.append(user.id)

        routes = Route.objects.all()[::-1]
        demo_route = routes[drone_id-1]
        way_points = WayPoint.objects.filter(route=demo_route)
        way_points = filter(lambda w: w.visited is False, way_points)
        c = AESCipher(shared_key)

        for wp in way_points:
            s = self.scan()
            p = None

            print (s, beacons)

            if s in beacons:
                p = self.take_photo()

            d = c.encrypt(json.dumps(({'id': wp.id, 'scan': s, 'photo': p})))
            requests.post(url_post, data={'droneId': drone_id, 'info': d})
            sleep(5)
