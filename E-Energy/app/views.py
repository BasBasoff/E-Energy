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
    def __init__(self, adapter_name, par_name, data=[]):
        self.id = id
        self.adapter_name = adapter_name
        self.par_name = par_name
        self.data = data

@login_required
def entrances(request, device_id):
    #device = Devices.objects.get(device_id = device_id)

    adapters_in = Adapters.objects.filter(id_device_id = device_id, adapter_name__icontains = 'вход').values_list('id_adapter', flat=True)
    adapters_out = Adapters.objects.filter(id_device_id = device_id, adapter_name__icontains = 'выход').values_list('id_adapter', flat=True)

    for a in adapters_in:
        param_current_in_A = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'ток фазы 1').values('id_parameter')
        param_current_in_B = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'ток фазы 2').values('id_parameter')
        param_current_in_C = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'ток фазы 3').values('id_parameter')

        param_voltage_in_A = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'напряжение фазы 1')
        param_voltage_in_B = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'напряжение фазы 2')
        param_voltage_in_C = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'напряжение фазы 3')

    for a in adapters_out:
        param_current_out_A = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'ток фазы 1').values('id_parameter')
        param_current_out_B = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'ток фазы 2').values('id_parameter')
        param_current_out_C = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'ток фазы 3').values('id_parameter')

        param_voltage_out_A = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'напряжение фазы 1')
        param_voltage_out_B = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'напряжение фазы 2')
        param_voltage_out_C = AdapterParameters.objects.filter(id_adapter = a).filter(parameter_name__icontains = 'напряжение фазы 3')

    #param_current_in_A = list(AdapterParameters.objects.filter(id_adapter__in = adapters_in).filter(parameter_name__icontains = 'ток фазы 1').values('id_parameter', 'parameter_name'))
    #data = Data.objects.filter(id_parameter = param_current_in_A[id_parameter]).values('measure_value', 'id_parameter')
    #current_in_A = Entrance('вход', param_current_in_A.parameter_name, data)

    #param_current_in_B = AdapterParameters.objects.filter(id_adapter__in = adapter_in.id_adapter).filter(parameter_name__icontains = 'ток фазы 2', )
    #data = Data.objects.filter(id_parameter = param_current_in_B.id_parameter).values_list('measure_value', flat=True)
    #current_in_B = Entrance('вход', param_current_in_B.parameter_name, data)
    #
    #param_current_in_C = AdapterParameters.objects.filter(id_adapter__in = adapter_in.id_adapter).filter(parameter_name__icontains = 'ток фазы 3', )
    #data = Data.objects.filter(id_parameter = param_current_in_C.id_parameter).values_list('measure_value', flat=True)
    #current_in_C = Entrance('вход', param_current_in_C.parameter_name, data)
    #
    #param_voltage_in_A = AdapterParameters.objects.filter(id_adapter__in = adapter_in.id_adapter).filter(parameter_name__icontains = 'напряжение фазы 1', )
    #data = Data.objects.filter(id_parameter = param_voltage_in_A.id_parameter).values_list('measure_value', flat=True)
    #voltage_in_A = Entrance('вход', param_voltage_in_A.parameter_name, data)
    #
    #param_voltage_in_B = AdapterParameters.objects.filter(id_adapter__in = adapter_in.id_adapter).filter(parameter_name__icontains = 'напряжение фазы 2', )
    #data = Data.objects.filter(id_parameter = param_voltage_in_B.id_parameter).values_list('measure_value', flat=True)
    #voltage_in_B = Entrance('вход', param_voltage_in_B.parameter_name, data)
    #
    #param_voltage_in_C = AdapterParameters.objects.filter(id_adapter__in = adapter_in.id_adapter).filter(parameter_name__icontains = 'напряжение фазы 3', )
    #data = Data.objects.filter(id_parameter = param_voltage_in_C.id_parameter).values_list('measure_value', flat=True)
    #voltage_in_C = Entrance('вход', param_voltage_in_C.parameter_name, data)
    #
    #
    #param_current_out_A = AdapterParameters.objects.filter(id_adapter__in = adapter_out.id_adapter).filter(parameter_name__icontains = 'ток фазы 1', )
    #data = Data.objects.filter(id_parameter = param_current_out_A.id_parameter).values_list('measure_value', flat=True)
    #current_out_A = Entrance('выход', param_current_out_A.parameter_name, data)
    #
    #param_current_out_B = AdapterParameters.objects.filter(id_adapter__in = adapter_out.id_adapter).filter(parameter_name__icontains = 'ток фазы 2', )
    #data = Data.objects.filter(id_parameter = param_current_out_B.id_parameter).values_list('measure_value', flat=True)
    #current_out_B = Entrance('выход', param_current_out_B.parameter_name, data)
    #
    #param_current_out_C = AdapterParameters.objects.filter(id_adapter__in = adapter_out.id_adapter).filter(parameter_name__icontains = 'ток фазы 3', )
    #data = Data.objects.filter(id_parameter = param_current_out_C.id_parameter).values_list('measure_value', flat=True)
    #current_out_C = Entrance('выход', param_current_out_C.parameter_name, data)
    #
    #param_voltage_out_A = AdapterParameters.objects.filter(id_adapter__in = adapter_out.id_adapter).filter(parameter_name__icontains = 'напряжение фазы 1', )
    #data = Data.objects.filter(id_parameter = param_voltage_out_A.id_parameter).values_list('measure_value', flat=True)
    #voltage_out_A = Entrance('выход', param_voltage_out_A.parameter_name, data)
    #
    #param_voltage_out_B = AdapterParameters.objects.filter(id_adapter__in = adapter_out.id_adapter).filter(parameter_name__icontains = 'напряжение фазы 2', )
    #data = Data.objects.filter(id_parameter = param_voltage_out_B.id_parameter).values_list('measure_value', flat=True)
    #voltage_out_B = Entrance('выход', param_voltage_out_B.parameter_name, data)
    #
    #param_voltage_out_C = AdapterParameters.objects.filter(id_adapter__in = adapter_out.id_adapter).filter(parameter_name__icontains = 'напряжение фазы 3', )
    #data = Data.objects.filter(id_parameter = param_voltage_out_C.id_parameter).values_list('measure_value', flat=True)
    #voltage_out_C = Entrance('выход', param_voltage_out_C.parameter_name, data)

    #for adap in adapter_list_in:
    #    for p in params_current_in = AdapterParameters.objects.filter(id_adapter__in = adap_list_in).filter(parameter_name__icontains = 'ток').values_list('id_parameter', flat=True)
    #params_voltage_in = AdapterParameters.objects.filter(id_adapter__in = adap_list_in).filter(parameter_name__icontains = 'напряжение').values_list('id_parameter', flat=True)
    #params_current_out = AdapterParameters.objects.filter(id_adapter__in = adap_list_out).filter(parameter_name__icontains = 'ток').values_list('id_parameter', flat=True)
    #params_voltage_out = AdapterParameters.objects.filter(id_adapter__in = adap_list_out).filter(parameter_name__icontains = 'напряжение').values_list('id_parameter', flat=True)
    #data_current_in = []
    #data_voltage_in = []
    #data_current_out = []
    #data_voltage_out = []
    #for adpater in adap_list_in:
    #    for data, param in zip([data_current_in, data_current_out,data_voltage_in,data_voltage_out],[params_current_in,params_current_out,params_voltage_in,params_voltage_out]):
    #        for p in param:
    #            data.append(list(Data.objects.filter(id_parameter = p).values_list('measure_value', flat=True)))
    #
    #data_current_in_json =  json.dumps(data_current_in)
    #data_voltage_in_json =  json.dumps(data_voltage_in)
    #data_current_out_json =  json.dumps(data_current_out)
    #data_voltage_out_json =  json.dumps(data_voltage_out)    
    return render(
        request,
        'app/entrances.html',        
        {
            'current_in_A':current_in_A,
            #'current_in_B':current_in_B,
            #'current_in_C':current_in_C,
            #'current_out_A':current_out_A,
            #'current_out_B':current_out_B,
            #'current_out_C':current_out_C,
            #'voltage_in_A':voltage_in_A,
            #'voltage_in_B':voltage_in_B,
            #'voltage_in_C':voltage_in_C,
            #'voltage_out_A':voltage_out_A,
            #'voltage_out_B':voltage_out_B,
            #'voltage_out_C':voltage_out_C,
            
            #'data_current_in' :data_current_in_json,
            #'data_voltage_in ':data_voltage_in_json, 
            #'data_current_out':data_current_out_json,
            #'data_voltage_out':data_voltage_out_json,            
        }
)