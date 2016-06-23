
from clients.models import Clients
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
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

        def post(self, request, *args, **kwargs):

            form_class = self.get_form_class()
            form = self.get_form(form_class)

            __post = self.request.POST.copy()

            try:
                if __post['c_insearch'] == 'on':
                    __post['insearch'] = True
            except:
                __post['insearch'] = False

            if form.is_valid():
                return self.form_valid(form, __post)

        def form_valid(self, form, post):

            import pprint

            self.object = form
            self.object.insearch = True

            print(help(self.object.Meta.fields.__hash__))

            #self.object.insearch = post['insearch']
            #self.object.save()

            #return super(EditClient, self).form_valid(form)
