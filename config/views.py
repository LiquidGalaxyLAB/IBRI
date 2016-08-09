
from clients.models import Clients
from drones.models import Drone
from search.models import Mission

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
from ibri.settings import GAPI
from ibri.settings import IBRI_URL

from utils.google import short_url

from requests import ConnectionError

import os


@staff_member_required
def viewMission(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    j = []
    for m in mission.inSearch.all():
        j.append(str(m.id))

    return render(request, 'pages/resume.html', {
        'mission': mission,
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
    return render(request, 'missions/mission_list.html', {
        'missionlist': Mission.objects.all()
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