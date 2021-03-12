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
    form = FilterForm()
    devices_dict = {}
    power_dict = {}

    for dev in devices:
        params_list = []		
        dev_adapters_params = AdapterParameters.objects.filter(id_adapter__in = dev.adapters.all()).select_related('id_adapter')
        #p_AU1 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 1',
        #                                id_adapter__adapter_name__icontains = 'вход',
        #                                )
        #p_BU1 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 2',
        #                                id_adapter__adapter_name__icontains = 'вход',
        #                                )
        #p_CU1 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 3',
        #                                id_adapter__adapter_name__icontains = 'вход',
        #                                )
        #
        #p_AI1 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 1',
        #                                id_adapter__adapter_name__icontains = 'вход',
        #                                )
        #p_BI1 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 2',
        #                                id_adapter__adapter_name__icontains = 'вход',
        #                                )
        #p_CI1 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 3',
        #                                id_adapter__adapter_name__icontains = 'вход',
        #                                )
        #
        #p_AU2 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 1',
        #                                id_adapter__adapter_name__icontains = 'выход',
        #                                )
        #p_BU2 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 2',
        #                                id_adapter__adapter_name__icontains = 'выход',
        #                                )
        #p_CU2 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 3',
        #                                id_adapter__adapter_name__icontains = 'выход',
        #                                )
        #
        #p_AI2 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 1',
        #                                id_adapter__adapter_name__icontains = 'выход',
        #                                )
        #p_BI2 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 2',
        #                                id_adapter__adapter_name__icontains = 'выход',
        #                                )
        #p_CI2 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 3',
        #                                id_adapter__adapter_name__icontains = 'выход',
        #                                )
        
        if request.method == 'POST':
            form = FilterForm(request.POST)
            if form.is_valid():
                date_from = form.cleaned_data['date_from']                
                date_to = form.cleaned_data['date_to']                
            else:
                return
        else:
            form = FilterForm() 
            date_to = CachingRecord.objects.filter(adapter_id__in = dev.adapters.all()).aggregate(
                                max_date=Max('record_time')
                            )['max_date']
            if date_to is None:
                continue
            date_from = date_to - timedelta(1) if date_to else None
        
        segmentation = 'hour'        
        
        #Params_by_hour = CachingRecord.objects.filter(
        #record_time__gte = date_from,
        #record_time__lte = date_to)\
        #    .annotate(
        #        data_date = Trunc('record_time', segmentation, tzinfo=None),
        #    ).values('data_date').annotate(
        #        p_AU1=Avg('measure_value', filter=Q(parameter_id = p_AU1.pk)),
        #        p_AI1=Avg('measure_value', filter=Q(parameter_id = p_AI1.pk)),
        #        p_BU1=Avg('measure_value', filter=Q(parameter_id = p_BU1.pk)),
        #        p_BI1=Avg('measure_value', filter=Q(parameter_id = p_BI1.pk)),
        #        p_CU1=Avg('measure_value', filter=Q(parameter_id = p_CU1.pk)),
        #        p_CI1=Avg('measure_value', filter=Q(parameter_id = p_CI1.pk)),
        #        p_AU2=Avg('measure_value', filter=Q(parameter_id = p_AU2.pk)),
        #        p_AI2=Avg('measure_value', filter=Q(parameter_id = p_AI2.pk)),
        #        p_BU2=Avg('measure_value', filter=Q(parameter_id = p_BU2.pk)),
        #        p_BI2=Avg('measure_value', filter=Q(parameter_id = p_BI2.pk)),
        #        p_CU2=Avg('measure_value', filter=Q(parameter_id = p_CU2.pk)),
        #        p_CI2=Avg('measure_value', filter=Q(parameter_id = p_CI2.pk)),                
        #        total_power = Avg('measure_value', filter=Q(parameter_id = p_AU1.pk))*Avg('measure_value', filter=Q(parameter_id = p_AI1.pk))*0.93 +
        #                      Avg('measure_value', filter=Q(parameter_id = p_BU1.pk))*Avg('measure_value', filter=Q(parameter_id = p_BI1.pk))*0.93 +
        #                      Avg('measure_value', filter=Q(parameter_id = p_CU1.pk))*Avg('measure_value', filter=Q(parameter_id = p_CI1.pk))*0.93,
        #        x1=Avg('measure_value', filter=Q(parameter_id = p_AI1.pk))*Avg('measure_value', filter=Q(parameter_id = p_AU2.pk))*0.93,
        #        x2=Avg('measure_value', filter=Q(parameter_id = p_AI2.pk))*Avg('measure_value', filter=Q(parameter_id = p_AU1.pk))*0.93,
        #        x3=Avg('measure_value', filter=Q(parameter_id = p_BI1.pk))*Avg('measure_value', filter=Q(parameter_id = p_BU2.pk))*0.93,
        #        x4=Avg('measure_value', filter=Q(parameter_id = p_BI2.pk))*Avg('measure_value', filter=Q(parameter_id = p_BU1.pk))*0.93,
        #        x5=Avg('measure_value', filter=Q(parameter_id = p_CI1.pk))*Avg('measure_value', filter=Q(parameter_id = p_CU2.pk))*0.93,
        #        x6=Avg('measure_value', filter=Q(parameter_id = p_CI2.pk))*Avg('measure_value', filter=Q(parameter_id = p_CU1.pk))*0.93,
        #    )

        Params_by_hour = CachingRecord.objects.filter(
        adapter_id__in = dev.adapters.all(),
        record_time__gte = date_from,
        record_time__lte = date_to)\
            .annotate(
                data_date = Trunc('record_time', segmentation, tzinfo=None),
            ).values('data_date').annotate(
                p_AU1=Avg('p_AU1'),
                p_AI1=Avg('p_AI1'),
                p_BU1=Avg('p_BU1'),
                p_BI1=Avg('p_BI1'),
                p_CU1=Avg('p_CU1'),
                p_CI1=Avg('p_CI1'),
                p_AU2=Avg('p_AU2'),
                p_AI2=Avg('p_AI2'),
                p_BU2=Avg('p_BU2'),
                p_BI2=Avg('p_BI2'),
                p_CU2=Avg('p_CU2'),
                p_CI2=Avg('p_CI2'),                
                total_power = Avg('total_power'),
                x0 = Avg('x0'),
                x8 = Avg('x8'),
                xp = Avg('xp')
            )
        Params_by_hour_list = list(Params_by_hour)        
        #   Суммирование мощности по фазам
        total_power = "{0:.3f}".format(sum([_['total_power'] for _ in Params_by_hour_list]))#Суммирование и округление до третьего знака
        #Рассчёт экономии
        XP = "{0:.3f}".format(sum([100-_['xp'] for _ in Params_by_hour_list])) #Экономия в Квт*ч
        XP_percent = "{0:.3f}".format(float(XP)/float(total_power)*100)
        #Подготовка данных для графика экономии
        for el in Params_by_hour_list:
            power_dict[str(el['data_date'].replace(tzinfo=None))] = "{0:.3}".format(100-(el['x0']/el['x8']*100))
        #Сбор данных напряжения и тока в таблицу
        #   Вход
        #last_record_in = CachingRecord.objects.filter(adapter_id__in = dev.adapters.all()).aggregate(
        #                        max_date=Max('record_time')
        #                    )['max_date']        
        AU1 = "{0:.3f}".format(Params_by_hour.last()['p_AU1'])
        BU1 = "{0:.3f}".format(Params_by_hour.last()['p_BU1'])
        CU1 = "{0:.3f}".format(Params_by_hour.last()['p_CU1'])
        AI1 = "{0:.3f}".format(Params_by_hour.last()['p_AI1'])
        BI1 = "{0:.3f}".format(Params_by_hour.last()['p_BI1'])
        CI1 = "{0:.3f}".format(Params_by_hour.last()['p_CI1'])
        #   Выход
        

        AU2 = "{0:.3f}".format(Params_by_hour.last()['p_AU2'])
        BU2 = "{0:.3f}".format(Params_by_hour.last()['p_BU2'])
        CU2 = "{0:.3f}".format(Params_by_hour.last()['p_CU2'])
        AI2 = "{0:.3f}".format(Params_by_hour.last()['p_AI2'])
        BI2 = "{0:.3f}".format(Params_by_hour.last()['p_BI2'])
        CI2 = "{0:.3f}".format(Params_by_hour.last()['p_CI2'])        
        devices_dict[dev.name] = {'pk':dev.pk,'values':{
                                                        'A_U1':AU1, 'A_I1':AI1, 'A_U2':AU2, 'A_I2':AI2,
                                                        'B_U1':BU1, 'B_I1':BI1, 'B_U2':BU2, 'B_I2':BI2,
                                                        'C_U1':CU1, 'C_I1':CI1, 'C_U2':CU2, 'C_I2':CI2,
                                                        'total_power': total_power,
                                                        'XP': XP, 'XP_percent':XP_percent
                                                        }
                                  }    
    power_json = []
    power_json = json.dumps(power_dict)
    return render(
        request,
        'app/index.html',
        {
            'title':'KF-Energy',
            'form': form,
            'devices':devices_dict,
            'power_array': power_json
        }
    )

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

@login_required
def entrances(request, device):
    data_dict = defaultdict(dict)      

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
        records_startdate = records_maxdate - timedelta(1) if records_maxdate else None
       
    _data_id_links = {}
    parameters = AdapterParameters.objects.select_related('id_adapter').filter(
        Q(id_adapter__device=device) &
        (Q(parameter_name__icontains = 'Ток') | Q(parameter_name__icontains = 'Напряжение'))
    )
    for p in parameters:
        _data_id_links[p.id_parameter] = p.id_adapter.adapter_name, p.parameter_name
    _data = defaultdict(list)

    if records_maxdate - records_startdate <= timedelta(hours=3):
        segmentation = 'minute'
    elif (records_maxdate - records_startdate > timedelta(hours=3)) & (records_maxdate - records_startdate <= timedelta(days=7)):  
        segmentation = 'hour'
    elif (records_maxdate - records_startdate > timedelta(days=7)) & (records_maxdate - records_startdate <= timedelta(weeks=14)):
        segmentation = 'day'
    elif (records_maxdate - records_startdate > timedelta(weeks=14)) & (records_maxdate - records_startdate <= timedelta(weeks=28*3)):
        segmentation = 'week'
    elif (records_maxdate - records_startdate > timedelta(weeks=28*3)) & (records_maxdate - records_startdate <= timedelta(weeks=28*15)):
        segmentation = 'month'
    else:
        segmentation = 'year'


    data_query = CachingRecord.objects.filter(
                            id_record__id_adapter__device=device, 
                            id_record__record_time__gte=records_startdate, 
                            id_record__record_time__lte=records_maxdate,
                            id_parameter__in=parameters.values('id_parameter'))\
                        .annotate(data_date=Trunc('id_record__record_time', segmentation, tzinfo=None))\
                        .prefetch_related('id_record')\
                        .values('id_parameter', 'data_date', 'id_record__id_adapter')\
                        .annotate(measure_value=Avg('measure_value'))
    for d in data_query.iterator():        
        _data[d['id_parameter']].append({'y': float(d['measure_value']), 'x': d['data_date'].replace(tzinfo=None)})
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
