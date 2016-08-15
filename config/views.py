
from clients.models import Clients
from drones.models import Drone
from search.models import Mission, Route, WayPoint

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.forms import forms
from django.views.generic.list import ListView
from ibri.settings import GAPI, IBRI_URL, KML_DIR

from utils.google import short_url

from requests import ConnectionError

from wsgiref.util import FileWrapper

import os


def downloadfile(request, m, r):
    filename = os.path.join(KML_DIR, 'IBRI'+m, 'IBRI'+m+'R'+r+'.kml')
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='application/vnd.google-earth.kml+xml')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
    response['Content-Length'] = os.path.getsize(filename)
    return response

@staff_member_required
def viewMission(request, pk):
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
    return render(request, 'pages/config/config.html')


def missionList(request):

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
    template_name = 'missions/delete.html'
    model = Mission
    success_url = reverse_lazy('missionlist')

def DroneList(request):
    return render(request, 'drones/drone_list.html', {
        'dronelist': Drone.objects.all()
    })

class DroneDelete(DeleteView):
    template_name = 'drones/delete.html'
    model = Drone
    success_url = reverse_lazy('dronelist')

class DroneCreate(CreateView):
    model = Drone
    fields = '__all__'
    success_message = "%(droneRef)s was created successfully"
    success_url = reverse_lazy('createdrone')

class EditDrone(UpdateView):
    model = Drone
    fields = '__all__'

    def get_success_url(self):
        return reverse('dronelist')


class CreateClient(SuccessMessageMixin, CreateView):

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

        request.POST = request.POST.copy()
        try:
            if request.POST['c_insearch'] == 'on':
                request.POST['insearch'] = True
        except:
            request.POST['insearch'] = False

        return super(CreateClient, self).post(request, **kwargs)


    @receiver(post_save, sender=Clients)
    def assignGoogleUrl(sender, instance, created, **kwargs):
        if created:
            print "User added "+str(instance.pk)
            googleUrl = os.path.dirname(IBRI_URL)+reverse('getclientdataweb', args=(instance.pk, ))
            
            try:
                gurl = short_url(googleUrl)
                instance.physicalCode = gurl
            except ConnectionError as e:
                instance.physicalCode = 'Google shortener connection error'

            instance.save()


class ListClient(ListView):

    model = Clients

    def get_context_data(self, **kwargs):
        context = super(ListClient, self).get_context_data(**kwargs)
        return context



class ClientDelete(DeleteView):
    model = Clients
    success_url = reverse_lazy('listclients')



class EditClient(SuccessMessageMixin, UpdateView):

        model = Clients
        fields = [
            'name',
            'lastname',
            'email',
            'identifier',
            'physicalCode',
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
                googleUrl = os.path.dirname(IBRI_URL)+reverse('getclientdataweb', args=(self.kwargs['pk'], ))
                
                try:
                    gurl = short_url(googleUrl)
                    self.object.physicalCode = gurl
                except ConnectionError as e:
                    messages
                    self.object.physicalCode = 'Google shortener connection error'
                except KeyError as k:
                    self.object.physicalCode = 'Google shortener key id error'


            self.object.save()
            return super(EditClient, self).form_valid(form)