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
from django.db.models.functions import Trunc
from collections import defaultdict
from datetime import datetime

from .forms import FilterForm
from .models import *

@login_required
def home(request):
    devices = Device.objects.filter(devices__profile__user_auth_id = request.user.id)
    devices_dict = {}

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

        last_record_in = Records.objects.filter(id_adapter = dev.adapters.first()).last()
        last_record_out = Records.objects.filter(id_adapter = dev.adapters.last()).last()
        
        if request.method == 'POST':
            form = FilterForm(request.POST)
            if form.is_valid():
                date_from = form.cleaned_data['date_from']                
                date_to = form.cleaned_data['date_to']                
            else:
                return
        else:
            form = FilterForm() 
            date_to = Records.objects.filter(id_adapter = dev.adapters.first()).aggregate(
                                max_date=Max('record_time')
                            )['max_date']
            date_from = date_to - timedelta(1) if date_to else None
        
        #Сбор данных полной мощности
        #   Вход
        #AU1_query = Data.objects.filter(id_parameter = p_AU1.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
        #    .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
        #    .values('data_date')\
        #    .annotate(avg_data=Avg('measure_value'))['avg_data']
        AU1_query = Data.objects.filter(id_parameter = p_AU1.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)           
        BU1_query = Data.objects.filter(id_parameter = p_BU1.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        CU1_query = Data.objects.filter(id_parameter = p_CU1.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        AI1_query = Data.objects.filter(id_parameter = p_AI1.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        BI1_query = Data.objects.filter(id_parameter = p_BI1.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        CI1_query = Data.objects.filter(id_parameter = p_CI1.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        #   Выход
        AU2_query = Data.objects.filter(id_parameter = p_AU2.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        BU2_query = Data.objects.filter(id_parameter = p_BU2.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        CU2_query = Data.objects.filter(id_parameter = p_CU2.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        AI2_query = Data.objects.filter(id_parameter = p_AI2.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        BI2_query = Data.objects.filter(id_parameter = p_BI2.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        CI2_query = Data.objects.filter(id_parameter = p_CI2.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to)\
            .annotate(data_date = Trunc('id_record__record_time', 'hour'))\
            .values('data_date')\
            .annotate(avg_data=Avg('measure_value')).values_list('avg_data', flat=True)
        #CI2_query = Data.objects.filter(id_parameter = p_CI2.pk, id_record__record_time__gte = date_from, id_record__record_time__lte = date_to).values_list('measure_value', flat=True)
        #   Суммирование произведений напряжения и тока
        A_power = sum(x*y*0.92 for x,y in zip(AU1_query, AI1_query))
        B_power = sum(x*y*0.92 for x,y in zip(BU1_query, BI1_query))
        C_power = sum(x*y*0.92 for x,y in zip(CU1_query, CI1_query))
        total_power = "{0:.3f}".format(float(sum([A_power, B_power, C_power]))/60) #Суммирование и округление до третьего знака
        #Рассчёт экономии
        x1 = sum(x*y*0.92 for x,y in zip(AI1_query, AU2_query))
        x2 = sum(x*y*0.92 for x,y in zip(AI2_query, AU1_query))
        x3 = sum(x*y*0.92 for x,y in zip(BI1_query, BU2_query))
        x4 = sum(x*y*0.92 for x,y in zip(BI2_query, BU1_query))
        x5 = sum(x*y*0.92 for x,y in zip(CI1_query, CU2_query))
        x6 = sum(x*y*0.92 for x,y in zip(CI2_query, CU2_query))
        x0 = sum([x1, x3, x5])
        x8 = sum([x2, x4, x6])
        XH = x0/x8*100
        XP = 100-XH #Экономия в Квт*ч        
        
        #Сбор данных напряжения и тока в таблицу
        #   Вход
        AU1 = Data.objects.get(id_parameter = p_AU1.pk, id_record = last_record_in.pk).measure_value
        #AU1 = Data.objects.get(id_parameter = p_AU1.pk, id_record = last_record_in.pk).measure_value
        BU1 = Data.objects.get(id_parameter = p_BU1.pk, id_record = last_record_in.pk).measure_value
        CU1 = Data.objects.get(id_parameter = p_CU1.pk, id_record = last_record_in.pk).measure_value
        AI1 = Data.objects.get(id_parameter = p_AI1.pk, id_record = last_record_in.pk).measure_value
        BI1 = Data.objects.get(id_parameter = p_BI1.pk, id_record = last_record_in.pk).measure_value
        CI1 = Data.objects.get(id_parameter = p_CI1.pk, id_record = last_record_in.pk).measure_value
        #   Выход
        AU2 = Data.objects.get(id_parameter = p_AU2.pk, id_record = last_record_out.pk).measure_value
        BU2 = Data.objects.get(id_parameter = p_BU2.pk, id_record = last_record_out.pk).measure_value
        CU2 = Data.objects.get(id_parameter = p_CU2.pk, id_record = last_record_out.pk).measure_value
        AI2 = Data.objects.get(id_parameter = p_AI2.pk, id_record = last_record_out.pk).measure_value
        BI2 = Data.objects.get(id_parameter = p_BI2.pk, id_record = last_record_out.pk).measure_value
        CI2 = Data.objects.get(id_parameter = p_CI2.pk, id_record = last_record_out.pk).measure_value
        
        devices_dict[dev.name] = {'pk':dev.pk,'values':{'A_U1':AU1, 'A_I1':AI1, 'A_U2':AU2, 'A_I2':AI2, 
                                                        'B_U1':BU1, 'B_I1':BI1, 'B_U2':BU2, 'B_I2':BI2, 
                                                        'C_U1':CU1, 'C_I1':CI1, 'C_U2':CU2, 'C_I2':CI2,
                                                        'total_power': total_power,
                                                        'XP': XP,
                                                        }}


    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'form': form,
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