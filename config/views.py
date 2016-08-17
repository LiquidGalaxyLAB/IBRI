#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  This file contains the views corresponding to the admin area.
"""

# Metadata
__author__ = 'Moises Lodeiro Santiago'
__credits__ = ['Moises Lodeiro-Santiago']
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = 'Moises Lodeiro-Santiago'
__email__ = "moises.lodeiro[at]gmail.com"
__status__ = "Production"

# Python imports
import os

# Django Imports
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.forms import forms
from django.views.generic.list import ListView

# Third party imports
from requests import ConnectionError
from wsgiref.util import FileWrapper

# Own imports
from ibri.settings import *
from clients.models import Clients
from drones.models import Drone
from search.models import Mission, Route, WayPoint
from ibri.settings import GAPI, IBRI_URL, KML_DIR
from utils.google import short_url


def downloadfile(request, m, r):
    """
    Download File returns an KML filename as petition. The files have the
    following format: IBRI[m]R[r].kml where the m is the mission id and the
    r is the route id.

    @param request: Request petition that is handled by Django
    @param m: Represents the mission id
    @param r: Represents the route id
    @see FileWrapper
    @see Content-Disposition
    """

    filename = os.path.join(KML_DIR, 'IBRI' + m, 'IBRI' + m + 'R' + r + '.kml')
    wrapper = FileWrapper(file(filename))
    ct = 'application/vnd.google-earth.kml+xml'
    response = HttpResponse(wrapper, content_type=ct)
    cd = 'attachment; filename=%s' % os.path.basename(filename)
    response['Content-Disposition'] = cd
    response['Content-Length'] = os.path.getsize(filename)
    return response


@staff_member_required
def viewMission(request, pk):
    """
    View Mission is called from the administration panel when
    an operator wants to see the results of one mission. Requires
    to have setted the Google API to use the Google Maps.

    @param request: Request petition that is handled by Django
    @param pk: Mission identifier
    """

    mission = get_object_or_404(Mission, pk=pk)
    j = []
    for m in mission.inSearch.all():
        j.append(str(m.id))

    routes = Route.objects.filter(mission=mission)

    return render(request, 'pages/resume.html', {
        'mission': mission,
        'based': routes[0],
        'insearch': mission.inSearch.all(),
        'selected': ','.join(j),
        'section': 'View Mission Results',
        'GAPI': GAPI,
        'norepeat': True
    })


@staff_member_required
def config_area(request):
    """
    Config area returns the render response of
    pages/config/config.html which represents the main admin zone.

    @param request: Request petition that is handled by Django
    """
    return render(request, 'pages/config/config.html')


def missionList(request):
    """
    Mission List returns a rendered html HttpResponse with the mission
    list stored in the database.

    @param request: Request petition that is handled by Django
    """

    m = list(Mission.objects.all())
    for i in range(0, len(m)):
        m[i].route = []

    for i in Route.objects.all():
        element = [e for e in m if e.id == i.mission.id]
        element[0].route.append(i.id)

    return render(request, 'missions/mission_list.html', {
        'missionlist': m[::-1]
    })


class MissionDelete(DeleteView):
    """
    Mission Delete uses DeleteView Django Class-Based to manage
    the object deleting.

    @ivar template_name: Route to the HTML template
    @ivar model: Referenced model
    @ivar success_url: Page that will be show if object is deleted
    @see: reverse_lazy
    """

    template_name = 'missions/delete.html'
    model = Mission
    success_url = reverse_lazy('missionlist')


def DroneList(request):
    """
    Drone List returns a rendered HttpResponse to show the
    drone list stored in the database.

    @param request: Request petition that is handled by Django
    """
    return render(request, 'drones/drone_list.html', {
        'dronelist': Drone.objects.all()
    })


class DroneDelete(DeleteView):
    """
    Drone Delete uses DeleteView Django Class-Based to manage
    the object deleting.

    @ivar template_name: Route to the HTML template
    @ivar model: Referenced model
    @ivar success_url: Page that will be show if object is deleted
    @see: reverse_lazy
    """
    template_name = 'drones/delete.html'
    model = Drone
    success_url = reverse_lazy('dronelist')


class DroneCreate(CreateView):
    """
    Drone Create uses DeleteView Django Class-Based to manage
    the object creating.

    @ivar fields: Model fields that will be show in the creation form
    @ivar model: Referenced model
    @ivar success_url: Page that will be show if object is deleted
    @ivar succes_message: The success message that will be display
    if user is saved correctly
    @see: reverse_lazy
    """
    model = Drone
    fields = '__all__'
    success_message = "%(droneRef)s was created successfully"
    success_url = reverse_lazy('createdrone')


class EditDrone(UpdateView):
    """
    Edit Drone uses UpdateView Django Class-Based to manage
    the object update.

    @ivar model: Referenced model
    @ivar fields: Model fields that will be show in the creation form
    @see: reverse_lazy
    """
    model = Drone
    fields = '__all__'

    def get_success_url(self):
        """
        Get Success URL returns the success url that the system
        will use when the model is edited.

        @param self: Self instance of the object
        """
        return reverse('dronelist')


class CreateClient(SuccessMessageMixin, CreateView):
    """
    Create Client extends two super classes. Those are SuccessMessageMixin
    that is to create a new success message when client is created and the
    CreateView Django Class-Based class to manage the object creating.

    @ivar model: Referenced model
    @ivar fields: Model fields that will be show in the creation form
    @ivar success_url: Page that will be show if object is deleted
    @ivar succes_message: The success message that will be display
    """

    model = Clients
    fields = [
        'name',
        'lastname',
        'email',
        'identifier',
        'address',
        'city',
        'mobileNumber',
        'birthDate',
        'postalCode',
        'alergies',
        'diseases',
        'bloodType',
        'insearch'
    ]

    success_message = "%(name)s was created successfully"
    success_url = reverse_lazy('createclient')

    def post(self, request, **kwargs):
        """
        Post method is the responsable to acquire the POST data from the
        form. To avoid a materialize.css checkbox display problem we
        override it to manually check if a checkbox named "c_insearch" is
        enabled or not.

        @param self: Self instance of the object
        @param request: Request information from the form
        @return: Super call to CreateClient class
        """

        request.POST = request.POST.copy()
        try:
            if request.POST['c_insearch'] == 'on':
                request.POST['insearch'] = True
        except:
            request.POST['insearch'] = False

        return super(CreateClient, self).post(request, **kwargs)

    @receiver(post_save, sender=Clients)
    def assignGoogleUrl(sender, instance, created, **kwargs):
        """
        Assign Google URL is the method that is triggered when
        post_save signal is emitted. If the user hasn't got assigned
        a URL the system will modify the physicalCode to set the new
        shortened URL.

        @param sender: Instance of the sender class
        @param instance: Self instance
        @param created: Boolean field that tell us if the user has been
        created
        """

        if created:

            if settings.DEBUG:
                print "User added " + str(instance.pk)

            rev = reverse('getclientdataweb', args=(instance.pk, ))
            googleUrl = os.path.dirname(IBRI_URL) + rev

            try:
                gurl = short_url(googleUrl)
                instance.physicalCode = gurl
            except ConnectionError as e:
                print colored(e, 'red')
                instance.physicalCode = 'Google shortener connection error'

            instance.save()


class ListClient(ListView):
    """
    List Client exrends ListView Django Class-Based to list the
    elements that corresponds to Clients Model

    @ivar model: Referenced model
    """

    model = Clients

    def get_context_data(self, **kwargs):
        """
        Get Context Data returns the actual actual context

        @param self: Self instance of the object.
        """

        context = super(ListClient, self).get_context_data(**kwargs)
        return context



class ClientDelete(DeleteView):
    """
    Client Delete uses DeleteView Django Class-Based to manage
    the object deleting.

    @ivar model: Referenced model
    @ivar success_url: Page that will be show if object is deleted
    @see: reverse_lazy
    """
    model = Clients
    success_url = reverse_lazy('listclients')



class EditClient(SuccessMessageMixin, UpdateView):
    """
    Edit Client uses UpdateView Django Class-Based to manage
    the object update. In this case we change __all__ value for
    the reference to each field name of the model.

    @ivar model: Referenced model
    @ivar fields: Model fields that will be show in the creation form
    @ivar succes_message: The success message that will be display
    @see: reverse_lazy
    """

    model = Clients
    fields = [
        'name', 'lastname', 'email', 'identifier', 'physicalCode',
        'address', 'city', 'mobileNumber', 'birthDate', 'postalCode',
        'alergies', 'diseases', 'bloodType', 'insearch'
    ]

    success_message = "%(name)s was modified successfully"

    def get_success_url(self):
        return reverse('editclient', args=(self.kwargs['pk'],))

    def form_valid(self, form):

        try:
            if self.request.POST['c_insearch'] == 'on':
                self.object.insearch = True
        except:
            self.object.insearch = False

        if self.object.physicalCode == "":
            rev = reverse('getclientdataweb', args=(self.kwargs['pk'], ))
            googleUrl = os.path.dirname(IBRI_URL) + rev

            try:
                gurl = short_url(googleUrl)
                self.object.physicalCode = gurl
            except ConnectionError as e:
                print colored(e, 'red')
                self.object.physicalCode = 'Google shortener connection error'
            except KeyError as k:
                print colored(k, 'red')
                self.object.physicalCode = 'Google shortener key id error'

        self.object.save()
        return super(EditClient, self).form_valid(form)
