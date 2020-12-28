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
    #parameters = ['Полная мощность']
    #measures = list(Data.objects.filter(id_parameter__in=parameters).filter(id_record__id_adapter__id_device=device.device_id))
    #measures_json = serializers.serialize('json', measures)
    #measures_json_string = str(measures_json)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            #'values':measures_json,
            #'measures':measures_json_string,
            #'values':measures_json_string,
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

class Entrance():
    def __init__(self, inp, out):
        self.inp = inp
        self.out = out
        self.id = id

def entrances(request):
    user = Users.objects.get(id_user=request.user.id)
    devices = Devices.objects.filter(devicestouser__id_user = user.id_user)
    param_id_in = AdapterParameters.objects.filter(adapter__devices__devicestouser__id_user = user.id).filter(adapter__adapter_name__icontains = 'вход').values('id_parameter')
    param_id_out = AdapterParameters.objects.filter(adapter__devices__devicestouser__id_user = user.id).filter(adapter__adapter_name__icontains = 'выход').values('id_parameter')
    data_in = Data.objects.filter(id_parameter = param_id_in.id_parameter).value('measure_value')
    data_out = Data.objects.filter(id_parameter = param_id_out.id_parameter).value('measure_value')
    data = Entrance(data_in.measure_value, data_out.measure_value)
    return render(
        request,
        'app/entrances.html',
        {
            'entrance':data
        }
)