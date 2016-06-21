
from clients.models import Clients
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView

from django.forms import forms


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
        'physicalCode',
        'address',
        'city',
        'mobileNumber',
        'birthDate',
        'postalCode',
        'alergies',
        'diseases',
        'contacts',
        'bloodType'
    ]

    success_message = "%(name)s was created successfully"
    success_url = reverse_lazy('createclient')




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
            'contacts',
            'bloodType'
        ]

        success_message = "%(name)s was modified successfully"

        def get_context_data(self, **kwargs):
            context = super(EditClient, self).get_context_data(**kwargs)
            context['client'] = self.object
            return context

        def get_success_url(self):
            return reverse('editclient', args=(self.object.pk,))

        def form_valid(self, form):
            print form