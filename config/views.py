from clients.models import Clients
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView


@staff_member_required
def config_area(request):
    return HttpResponse('TODO')

class CreateClient(CreateView):
    model = Clients
    fields = '__all__'
    success_url = reverse_lazy('createclient')

class EditClient(UpdateView):
        model = Clients
        fields = '__all__'
        success_url = reverse_lazy('editclient')

        #def create_client(request):
#    form = ClientForm()
#    return render(request, 'pages/form.html', {'form' : form})


#def edit_client(request):
#    form = ClientForm(pk=1)
#    return render(request, 'pages/form.html', {'form' : form})