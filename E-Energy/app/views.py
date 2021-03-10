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
        p_AU1 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 1',
                                        id_adapter__adapter_name__icontains = 'вход',
                                        )
        p_BU1 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 2',
                                        id_adapter__adapter_name__icontains = 'вход',
                                        )
        p_CU1 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 3',
                                        id_adapter__adapter_name__icontains = 'вход',
                                        )
        
        p_AI1 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 1',
                                        id_adapter__adapter_name__icontains = 'вход',
                                        )
        p_BI1 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 2',
                                        id_adapter__adapter_name__icontains = 'вход',
                                        )
        p_CI1 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 3',
                                        id_adapter__adapter_name__icontains = 'вход',
                                        )
        
        p_AU2 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 1',
                                        id_adapter__adapter_name__icontains = 'выход',
                                        )
        p_BU2 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 2',
                                        id_adapter__adapter_name__icontains = 'выход',
                                        )
        p_CU2 = dev_adapters_params.get(parameter_name__contains = 'Напряжение фазы 3',
                                        id_adapter__adapter_name__icontains = 'выход',
                                        )
        
        p_AI2 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 1',
                                        id_adapter__adapter_name__icontains = 'выход',
                                        )
        p_BI2 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 2',
                                        id_adapter__adapter_name__icontains = 'выход',
                                        )
        p_CI2 = dev_adapters_params.get(parameter_name__contains = 'Ток фазы 3',
                                        id_adapter__adapter_name__icontains = 'выход',
                                        )
        
        if request.method == 'POST':
            form = FilterForm(request.POST)
            if form.is_valid():
                date_from = form.cleaned_data['date_from']                
                date_to = form.cleaned_data['date_to']                
            else:
                return
        else:
            form = FilterForm() 
            date_to = CachingData.objects.filter(adapter_id = dev.adapters.last().id_adapter).aggregate(
                                max_date=Max('record_time')
                            )['max_date']
            if date_to is None:
                continue
            date_from = date_to - timedelta(1) if date_to else None
        
        segmentation = 'hour'        
        
        Params_by_hour = CachingData.objects.filter(
        record_time__gte = date_from,
        record_time__lte = date_to)\
            .annotate(
                data_date = Trunc('record_time', segmentation),
            ).values('data_date').annotate(
                p_AU1=Avg('measure_value', filter=Q(parameter_id = p_AU1.pk)),
                p_AI1=Avg('measure_value', filter=Q(parameter_id = p_AI1.pk)),
                p_BU1=Avg('measure_value', filter=Q(parameter_id = p_BU1.pk)),
                p_BI1=Avg('measure_value', filter=Q(parameter_id = p_BI1.pk)),
                p_CU1=Avg('measure_value', filter=Q(parameter_id = p_CU1.pk)),
                p_CI1=Avg('measure_value', filter=Q(parameter_id = p_CI1.pk)),
                p_AU2=Avg('measure_value', filter=Q(parameter_id = p_AU2.pk)),
                p_AI2=Avg('measure_value', filter=Q(parameter_id = p_AI2.pk)),
                p_BU2=Avg('measure_value', filter=Q(parameter_id = p_BU2.pk)),
                p_BI2=Avg('measure_value', filter=Q(parameter_id = p_BI2.pk)),
                p_CU2=Avg('measure_value', filter=Q(parameter_id = p_CU2.pk)),
                p_CI2=Avg('measure_value', filter=Q(parameter_id = p_CI2.pk)),
                A_power=Avg('measure_value', filter=Q(parameter_id = p_AU1.pk))*Avg('measure_value', filter=Q(parameter_id = p_AI1.pk))*0.93,
                B_power=Avg('measure_value', filter=Q(parameter_id = p_BU1.pk))*Avg('measure_value', filter=Q(parameter_id = p_BI1.pk))*0.93,
                C_power=Avg('measure_value', filter=Q(parameter_id = p_CU1.pk))*Avg('measure_value', filter=Q(parameter_id = p_CI1.pk))*0.93,
                x1=Avg('measure_value', filter=Q(parameter_id = p_AI1.pk))*Avg('measure_value', filter=Q(parameter_id = p_AU2.pk))*0.93,
                x2=Avg('measure_value', filter=Q(parameter_id = p_AI2.pk))*Avg('measure_value', filter=Q(parameter_id = p_AU1.pk))*0.93,
                x3=Avg('measure_value', filter=Q(parameter_id = p_BI1.pk))*Avg('measure_value', filter=Q(parameter_id = p_BU2.pk))*0.93,
                x4=Avg('measure_value', filter=Q(parameter_id = p_BI2.pk))*Avg('measure_value', filter=Q(parameter_id = p_BU1.pk))*0.93,
                x5=Avg('measure_value', filter=Q(parameter_id = p_CI1.pk))*Avg('measure_value', filter=Q(parameter_id = p_CU2.pk))*0.93,
                x6=Avg('measure_value', filter=Q(parameter_id = p_CI2.pk))*Avg('measure_value', filter=Q(parameter_id = p_CU1.pk))*0.93,
            )
        Params_by_hour_list = list(Params_by_hour)
        
        #   Суммирование мощности по фазам
        total_power = "{0:.3f}".format(sum([sum(_['A_power'] for _ in Params_by_hour_list),
                                            sum(_['B_power'] for _ in Params_by_hour_list),
                                            sum(_['C_power'] for _ in Params_by_hour_list)])) #Суммирование и округление до третьего знака
                 
        #Рассчёт экономии
        x0 = sum([sum(_['x1'] or 0 for _ in Params_by_hour), sum(_['x3'] or 0 for _ in Params_by_hour), sum(_['x5'] or 0 for _ in Params_by_hour)])
        x8 = sum([sum(_['x2'] or 0 for _ in Params_by_hour), sum(_['x4'] or 0 for _ in Params_by_hour), sum(_['x6'] or 0 for _ in Params_by_hour)])
        XH = x0/x8*100 if x8 != 0 else 0

        XP = "{0:.3f}".format(100-XH) #Экономия в Квт*ч
        #Подготовка данных для графика экономии
        for el in Params_by_hour_list:
            _X0 = sum([el['x1'], el['x3'], el['x5']])
            _X8 = sum([el['x2'], el['x4'], el['x6']])
            power_dict[str(el['data_date'].replace(tzinfo=None))] = "{0:.3}".format(100-(_X0/_X8*100))

        #Сбор данных напряжения и тока в таблицу
        #   Вход
        last_record_in = Records.objects.filter(id_adapter = dev.adapters.first()).last()
        last_datas = list(Data.objects.filter(id_record = last_record_in.pk))
        AU1 = next((item.measure_value for item in last_datas if item.id_parameter==p_AU1.pk), 0)
        BU1 = next((item.measure_value for item in last_datas if item.id_parameter==p_BU1.pk), 0)
        CU1 = next((item.measure_value for item in last_datas if item.id_parameter==p_CU1.pk), 0)
        AI1 = next((item.measure_value for item in last_datas if item.id_parameter==p_AI1.pk), 0)
        BI1 = next((item.measure_value for item in last_datas if item.id_parameter==p_BI1.pk), 0)
        CI1 = next((item.measure_value for item in last_datas if item.id_parameter==p_CI1.pk), 0)
        
		#AU1 = Data.objects.get(id_parameter = p_AU1.pk, id_record = last_record_in.pk).measure_value
        
		#BU1 = Data.objects.get(id_parameter = p_BU1.pk, id_record = last_record_in.pk).measure_value
        #CU1 = Data.objects.get(id_parameter = p_CU1.pk, id_record = last_record_in.pk).measure_value
        #AI1 = Data.objects.get(id_parameter = p_AI1.pk, id_record = last_record_in.pk).measure_value
        #BI1 = Data.objects.get(id_parameter = p_BI1.pk, id_record = last_record_in.pk).measure_value
        #CI1 = Data.objects.get(id_parameter = p_CI1.pk, id_record = last_record_in.pk).measure_value
        #   Выход
        last_record_out = Records.objects.filter(id_adapter = dev.adapters.last()).last()
        last_datas = list(Data.objects.filter(id_record = last_record_out.pk))
        
        AU2 = next((item.measure_value for item in last_datas if item.id_parameter==p_AU2.pk), 0)
        BU2 = next((item.measure_value for item in last_datas if item.id_parameter==p_BU2.pk), 0)
        CU2 = next((item.measure_value for item in last_datas if item.id_parameter==p_CU2.pk), 0)
        AI2 = next((item.measure_value for item in last_datas if item.id_parameter==p_AI2.pk), 0)
        BI2 = next((item.measure_value for item in last_datas if item.id_parameter==p_BI2.pk), 0)
        CI2 = next((item.measure_value for item in last_datas if item.id_parameter==p_CI2.pk), 0)		
		#AU2 = Data.objects.get(id_parameter = p_AU2.pk, id_record = last_record_out.pk).measure_value
        #BU2 = Data.objects.get(id_parameter = p_BU2.pk, id_record = last_record_out.pk).measure_value
        #CU2 = Data.objects.get(id_parameter = p_CU2.pk, id_record = last_record_out.pk).measure_value
        #AI2 = Data.objects.get(id_parameter = p_AI2.pk, id_record = last_record_out.pk).measure_value
        #BI2 = Data.objects.get(id_parameter = p_BI2.pk, id_record = last_record_out.pk).measure_value
        #CI2 = Data.objects.get(id_parameter = p_CI2.pk, id_record = last_record_out.pk).measure_value

        devices_dict[dev.name] = {'pk':dev.pk,'values':{
                                                        'A_U1':AU1, 'A_I1':AI1, 'A_U2':AU2, 'A_I2':AI2,
                                                        'B_U1':BU1, 'B_I1':BI1, 'B_U2':BU2, 'B_I2':BI2,
                                                        'C_U1':CU1, 'C_I1':CI1, 'C_U2':CU2, 'C_I2':CI2,
                                                        'total_power': total_power,
                                                        'XP': XP,                                                        
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
