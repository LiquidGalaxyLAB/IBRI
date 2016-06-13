from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
@staff_member_required
def config_area(request):
    return HttpResponse('TODO')