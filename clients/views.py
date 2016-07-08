from django.shortcuts import render, get_object_or_404


# Create your views here.


def showUserData(request, uid):

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