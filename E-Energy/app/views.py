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
def home(request):
    """Renders the home page."""
    assert isinstance(request,  HttpRequest)
    devices = Devices.objects.filter(profile__user_auth_id = request.user.id)

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
        parameters = AdapterParameters.objects.filter(parameter_name__icontains = 'Ток', id_adapter = a.id_adapter) 
        #| AdapterParameters.objects.filter(parameter_name__icontains = 'напряжение', id_adapter = a.id_adapter)
        for p in parameters:
            data = list(Data.objects.filter(id_parameter = p.id_parameter).values_list('measure_value', flat=True))
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