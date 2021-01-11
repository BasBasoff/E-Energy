"""
Definition of views.
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import *

@login_required
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

class Entrance():
    def __init__(self, inp, out):
        self.inp = inp
        self.out = out
        self.id = id

@login_required
def entrances(request, device=4):
    data_dict = {}
    adapters = Adapters.objects.filter(id_device = device)
    for a in adapters:
        parameters = AdapterParameters.objects.filter(parameter_name__icontains = 'ток') | AdapterParameters.objects.filter(parameter_name__icontains = 'напряжение')
        for p in parameters:
            data = Data.objects.filter(id_parameter = p.id_parameter).values_list('measure_value', flat=True)
            data_dict.update({a.adapter_name:{p.parameter_name:data}})

    
    return render(
        request,
        'app/entrances.html',
        {
            'data':data_dict,
            #'entrances':data,
            #'error':error
        }
)