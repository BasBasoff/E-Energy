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
def entrances(request):
    #user = Users.objects.get(id_user=request.user.id)
    error = None
#    try:
    

    #devices = Devices.objects.filter(profile__user_auth = request.user.id)
    #devices_id_list = []
    #for i in devices:
    #    devices_id_list.append(i.device_id)    
    #par_list = list(AdapterParameters.objects.filter(id_adapter__in = adp_id_list))
    #adap_list = Adapters.objects.filter(id_device_id__profile__user_auth = request.user.id)
    par_list = list(AdapterParameters.objects.filter(id_adapter__id_device_id__profile__user_auth = request.user.id, parameter_name__icontains = 'ток').values('id_parameter'))
    #par_id_list = []
    #for i in par_list:
    #    par_id_list.append(i.id_parameter)
    
    data = Data.objects.filter(id_parameter__in = par_list['id_parameter']).values('measure_value')
    #adap_list = Adapters.objects.filter(id_device_id__in = devices_id_list)
    #adp_id_list = []
    #for i in adap_list:
    #    adp_id_list.append(i.id_adapter)
    #data = Data.objects.filter(id_parameter__in = par_id_list)

    #param_id_in = AdapterParameters.objects.filter(id_adapter_id__devices__profile__user_auth_id = request.user.id).filter(adapter__adapter_name__icontains = 'вход').values('id_parameter')
    #param_id_out = AdapterParameters.objects.filter(devices__profile__user_auth = request.user.id).filter(adapter__adapter_name__icontains = 'выход').values('id_parameter')
    #data_in = Data.objects.filter(id_parameter = param_id_in.id_parameter).value('measure_value')
    #data_out = Data.objects.filter(id_parameter = param_id_out.id_parameter).value('measure_value')
    #data = Entrance(data_in.measure_value, data_out.measure_value)
#    except Exception:
#        data = Entrance(0,0)
#        error = 'У вас пока нет устройств для отображения'
    return render(
        request,
        'app/entrances.html',
        {
            'entrance':data,
            #'entrances':data,
            'error':error
        }
)