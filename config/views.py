
from clients.models import Clients
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView

from django.forms import forms
from django.views.generic.list import ListView


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


class ListClient(ListView):

    model = Clients

    def get_context_data(self, **kwargs):
        context = super(ListClient, self).get_context_data(**kwargs)
        #context['now'] = timezone.now()
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
            'contacts',
            'bloodType',
            'insearch'
        ]

        success_message = "%(name)s was modified successfully"

        def get_context_data(self, **kwargs):
            context = super(EditClient, self).get_context_data(**kwargs)
            context['client'] = self.object
            return context

        def get_success_url(self):
            return reverse('editclient', args=(self.object.pk,))

        def clean(self):
            print self
            return self.cleaned_data

        def form_valid(self, form):
            #form.instance.insearch = form.cleaned_data['insearch']
            print form.cleaned_data
            return super(EditClient, self).form_valid(form)
