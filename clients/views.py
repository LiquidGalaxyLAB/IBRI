#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  This file contains the functions that to manage the clients data
  as login or show user data.
"""

# Metadata
__author__ = 'Moises Lodeiro Santiago'
__credits__ = ['Moises Lodeiro-Santiago']
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = 'Moises Lodeiro-Santiago'
__email__ = "moises.lodeiro[at]gmail.com"
__status__ = "Production"

# Django Imports
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


def ulogin(request):
    """
    The ulogin function overide the login native function to get
    loged in the system.

    @param request: Request petition that is handled by Django
    @return: Render html page/login.html
    @return: HttpResponseRedirect user and password are correct
    @return: HttpResponse if not active
    @ivar username: Username (initialized in blank)
    @ivar password: Password (initialized in blank)
    """

    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.POST['next']:
                    return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponse("Error: User not active")

    return render(request, 'pages/login.html')


def showUserData(request, uid):
    """
    Show User Data is the function that renders the public user URL.

    This could be an empty webpage or an alert page that informs that an
    user us un missing state. If anyone has installed the physica web beacon
    official application will be notified if detects the beacon. 

    @param request: Request petition that is handled by Django
    @param uid: The uid is the url identifier that represents the user
    id.

    Example:
        - url: /p/5/ to get the information about user number 5.
    """

    from clients.models import Clients
    udata = get_object_or_404(Clients, pk=uid)

    if udata.insearch:
        return render(request, 'clients/clients_missing.html', context={
            'user': udata
        })
    else:
        return render(request, 'clients/clients_show.html', context={
            'user': udata
        })