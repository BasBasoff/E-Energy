"""
Definition of views.
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.core import serializers

from .models import *

def home(request, dev_id=4):
    """Renders the home page."""
    assert isinstance(request,  HttpRequest)
    #user = Users.objects.get(id_user=request.user.id_user)
    devices = Devices.objects.all()
    device = Devices.objects.get(device_id=dev_id)
    #adapter = picle(Adapters.objects.filter(id_device=device.device_id).values('id_adapter'))
    #record = list(Records.objects.filter(id_adapter__in=adapter.id_adapter).values('id_record'))
    parameters = []
    measures = Data.objects.filter(id_parameter__in=parameters).filter(id_record__id_adapter__id_device=device.device_id)
    measures_json = serializers.serialize('json', measures)
    measures_json_string = str(measures_json)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            #'values':measures_json,
            'measures':measures_json_string,
            'values':measures,
            'devices':devices
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
