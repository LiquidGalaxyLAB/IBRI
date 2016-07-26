
from clients.models import Clients
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView

from django.forms import forms
from django.views.generic.list import ListView

from ibri.settings import IBRI_URL
from utils.google import short_url

@staff_member_required
def config_area(request):
    return render(request, 'pages/config/config.html')



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
                    #self.object.save()
            except:
                self.object.insearch = False
            
            self.object.save()

            return super(EditClient, self).form_valid(form)

        @receiver(pre_save)
        def setPhysicalWeb(sender, instance, *args, **kwargs):

            if Clients.objects.get(pk=instance.pk).physicalCode == "":
                googleUrl = IBRI_URL+reverse('getclientdataweb', args=(instance.pk, ))
                gurl = short_url(googleUrl)
                instance.physicalCode = gurl
                

            #print args['email']

            #TODO: Get FULL url to get the google shorted url
            #googleUrl = reverse('getclientdataweb', args=(instance.pk, ))
            #print "PHYSICAL URL: "+googleUrl
            pass
            #instance.physicalCode = 'HOLA CARACOLA'