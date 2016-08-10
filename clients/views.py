from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


# Create your views here.

def ulogin(request):

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