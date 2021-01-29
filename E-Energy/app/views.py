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
from django.db.models import Q, FilteredRelation, Subquery, F, Prefetch, Count, Max
from collections import defaultdict


from .models import *

@login_required
def home(request):
    """Renders the home page."""
    devices = Devices.objects.filter(profile__user_auth_id = request.user.id)
    values_list = [1.5, 1.435, 1.330, 2, 1.1, 1.208, 1.7]
    values = json.dumps(values_list)
    if request.method == 'POST':
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']


    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'data':values,
            'devices':devices
        }
    )

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()
@login_required
def entrances(request, device, days=1):
    data_dict = defaultdict(dict)
    parameters = AdapterParameters.objects.select_related('id_adapter').filter(
        Q(id_adapter__id_device=device) &
        (Q(parameter_name__icontains = 'Ток') | Q(parameter_name__icontains = 'напряжение'))
    )
    
    records = Records.objects.filter(id_adapter__id_device=device)
    if request.method == 'POST':
        records_startdate = request.POST.get('date_from')
        records_maxdate = request.POST.get('date_to')
    #records_maxdate = Records.objects.filter(id_adapter__id_device=device).aggregate(
    #                max_date=Max('record_time')
    #            )['max_date']
    #records_startdate = records_maxdate - timedelta(days) if records_maxdate else None
    #if records_startdate:
    records = records.filter(record_time__gt=records_startdate, record_time__lt=records_maxdate)

    records = records.values_list('id_record', flat=True)
    _data_id_links = {}
    for p in parameters:
        _data_id_links[p.id_parameter] = p.id_adapter.adapter_name, p.parameter_name
    _data = defaultdict(list)
    for d in Data.objects.filter(id_record__in=records, id_parameter__in=parameters.values('id_parameter'))\
                        .prefetch_related('id_record').values(
        'measure_value', 'id_parameter', 'id_record__record_time', 'id_record__id_adapter'
    ).iterator():
        _data[d['id_parameter']].append({'y': float(d['measure_value']), 'x': int(d['id_record__record_time'].timestamp())*100})
    t2 = time()
    for k,v in _data.items():
        adapter_name, parameter_name = _data_id_links[k]
        data_dict[adapter_name][parameter_name] = json.dumps(v, default=myconverter)
    return render(
        request,
        'app/entrances.html',        
        {
            'data': dict(data_dict)
        }
    )