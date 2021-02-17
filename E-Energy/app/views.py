"""
Definition of views.
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from time import time
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpRequest
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db.models import Q, FilteredRelation, Subquery, F, Prefetch, Count, Max, Sum, Avg, Func
from collections import defaultdict
from datetime import datetime

from .forms import FilterForm
from .models import *

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'

@login_required
def home(request):
    devices = Device.objects.filter(devices__profile__user_auth_id = request.user.id)
    devices_dict = {}
    #values_list = [1.5, 1.435, 1.330, 2, 1.1, 1.208, 1.7]
    for dev in devices:
        p_AU1 = AdapterParameters.objects.get(parameter_name__contains = 'Напряжение фазы 1',
                                                 id_adapter__adapter_name__icontains = 'вход',
                                                 id_adapter__in = dev.adapters.all())
        p_BU1 = AdapterParameters.objects.get(parameter_name__contains = 'Напряжение фазы 2',
                                                 id_adapter__adapter_name__icontains = 'вход',
                                                 id_adapter__in = dev.adapters.all())
        p_CU1 = AdapterParameters.objects.get(parameter_name__contains = 'Напряжение фазы 3',
                                                 id_adapter__adapter_name__icontains = 'вход',
                                                 id_adapter__in = dev.adapters.all())

        p_AI1 = AdapterParameters.objects.get(parameter_name__contains = 'Ток фазы 1',
                                                 id_adapter__adapter_name__icontains = 'вход',
                                                 id_adapter__in = dev.adapters.all())
        p_BI1 = AdapterParameters.objects.get(parameter_name__contains = 'Ток фазы 2',
                                                 id_adapter__adapter_name__icontains = 'вход',
                                                 id_adapter__in = dev.adapters.all())
        p_CI1 = AdapterParameters.objects.get(parameter_name__contains = 'Ток фазы 3',
                                                 id_adapter__adapter_name__icontains = 'вход',
                                                 id_adapter__in = dev.adapters.all())

        p_AU2 = AdapterParameters.objects.get(parameter_name__contains = 'Напряжение фазы 1',
                                                 id_adapter__adapter_name__icontains = 'выход',
                                                 id_adapter__in = dev.adapters.all())
        p_BU2 = AdapterParameters.objects.get(parameter_name__contains = 'Напряжение фазы 2',
                                                 id_adapter__adapter_name__icontains = 'выход',
                                                 id_adapter__in = dev.adapters.all())
        p_CU2 = AdapterParameters.objects.get(parameter_name__contains = 'Напряжение фазы 3',
                                                 id_adapter__adapter_name__icontains = 'выход',
                                                 id_adapter__in = dev.adapters.all())

        p_AI2 = AdapterParameters.objects.get(parameter_name__contains = 'Ток фазы 1',
                                                 id_adapter__adapter_name__icontains = 'выход',
                                                 id_adapter__in = dev.adapters.all())
        p_BI2 = AdapterParameters.objects.get(parameter_name__contains = 'Ток фазы 2',
                                                 id_adapter__adapter_name__icontains = 'выход',
                                                 id_adapter__in = dev.adapters.all())
        p_CI2 = AdapterParameters.objects.get(parameter_name__contains = 'Ток фазы 3',
                                                 id_adapter__adapter_name__icontains = 'выход',
                                                 id_adapter__in = dev.adapters.all())

        last_record_in = Records.objects.filter(id_adapter = dev.adapters.first()).order_by('record_time').last()
        last_record_out = Records.objects.filter(id_adapter = dev.adapters.last()).order_by('record_time').last()

        A_U1 = Data.objects.get(id_parameter = p_AU1.pk, id_record = last_record_in.pk).measure_value
        B_U1 = Data.objects.get(id_parameter = p_BU1.pk, id_record = last_record_in.pk).measure_value
        C_U1 = Data.objects.get(id_parameter = p_CU1.pk, id_record = last_record_in.pk).measure_value
        A_I1 = Data.objects.get(id_parameter = p_AI1.pk, id_record = last_record_in.pk).measure_value
        B_I1 = Data.objects.get(id_parameter = p_BI1.pk, id_record = last_record_in.pk).measure_value
        C_I1 = Data.objects.get(id_parameter = p_CI1.pk, id_record = last_record_in.pk).measure_value
        
        A_U2 = Data.objects.get(id_parameter = p_AU2.pk, id_record = last_record_out.pk).measure_value
        B_U2 = Data.objects.get(id_parameter = p_BU2.pk, id_record = last_record_out.pk).measure_value
        C_U2 = Data.objects.get(id_parameter = p_CU2.pk, id_record = last_record_out.pk).measure_value
        A_I2 = Data.objects.get(id_parameter = p_AI2.pk, id_record = last_record_out.pk).measure_value
        B_I2 = Data.objects.get(id_parameter = p_BI2.pk, id_record = last_record_out.pk).measure_value
        C_I2 = Data.objects.get(id_parameter = p_CI2.pk, id_record = last_record_out.pk).measure_value
        
        devices_dict[dev.name] = {'pk':dev.pk,'values':{'A_U1':A_U1, 'A_I1':A_I1, 'A_U2':A_U2, 'A_I2':A_I2, 
                                                        'B_U1':B_U1, 'B_I1':B_I1, 'B_U2':B_U2, 'B_I2':B_I2, 
                                                        'C_U1':C_U1, 'C_I1':C_I1, 'C_U2':C_U2, 'C_I2':C_I2}}

        #p_Power = AdapterParameters.objects.get(parameter_name__contains = 'Полная мощность',
        #                                        id_adapter__adapter_name__icontains = 'вход',
        #                                        id_adapter__in = dev.adapters.all())
        #d_Power = Data.objects.filter(id_parameter = p_Power.pk)

    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
        else:
            return
    else:
        form = FilterForm()

    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'devices':devices_dict
        }
    )

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

@login_required
def entrances(request, device, days=1):
    data_dict = defaultdict(dict)    
    parameters = AdapterParameters.objects.select_related('id_adapter').filter(
        Q(id_adapter__device=device) &
        (Q(parameter_name__icontains = 'Ток') | Q(parameter_name__icontains = 'напряжение'))
    )
    
    records = Records.objects.filter(id_adapter__device=device)
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():            
            records_startdate = form.cleaned_data['date_from']
            records_maxdate = form.cleaned_data['date_to']
        else:
            return 
    else:
        form = FilterForm()
        records_maxdate = Records.objects.filter(id_adapter__device=device).aggregate(
                        max_date=Max('record_time')
                    )['max_date']
        records_startdate = records_maxdate - timedelta(days) if records_maxdate else None
    
    records = records.filter(record_time__gte=records_startdate, record_time__lte=records_maxdate)
    records = records.values_list('id_record', flat=True)
    _data_id_links = {}
    for p in parameters:
        _data_id_links[p.id_parameter] = p.id_adapter.adapter_name, p.parameter_name
    _data = defaultdict(list)
    for d in Data.objects.filter(id_record__in=records, id_parameter__in=parameters.values('id_parameter'))\
                        .prefetch_related('id_record').values(
        'measure_value', 'id_parameter', 'id_record__record_time', 'id_record__id_adapter'
    ).iterator():
        _data[d['id_parameter']].append({'y': float(d['measure_value']), 'x': d['id_record__record_time'].replace(tzinfo=None)})
    t2 = time()
    for k,v in _data.items():
        adapter_name, parameter_name = _data_id_links[k]
        data_dict[adapter_name][parameter_name] = json.dumps(v, default=myconverter)
    return render(
        request,
        'app/entrances.html',        
        {
            'data': dict(data_dict),
            'form':form,
            'device': device
        }
    )