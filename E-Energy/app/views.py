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

from .models import *

@login_required
def home(request):
    devices = Device.objects.filter(devices__profile__user_auth_id = request.user.id)
    devices_dict = {}
    power_dict = {}

    for dev in devices:
        params_list = []		
        dev_adapters_params = AdapterParameters.objects.filter(id_adapter__in = dev.adapters.all()).select_related('id_adapter')
        
        if request.method == 'POST':
            date_from = datetime.strptime(request.POST['date_pick'].split(' ~ ')[0], '%Y-%m-%d %H:%M')                
            date_to = datetime.strptime(request.POST['date_pick'].split(' ~ ')[1], '%Y-%m-%d %H:%M')
        else:            
            date_to = CachingRecord.objects.filter(adapter_id__in = dev.adapters.all()).aggregate(
                                max_date=Max('record_time')
                            )['max_date']
            if date_to is None:
                continue
            date_from = date_to - timedelta(days=1) if date_to else None
        
        segmentation = 'hour'        
        
        Params_by_hour = CachingRecord.objects.filter(
        adapter_id__in = dev.adapters.all(),
        record_time__gte = date_from,
        record_time__lte = date_to)\
            .annotate(
                data_date = Trunc('record_time', segmentation, tzinfo=None),
            ).values('data_date', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6').annotate(
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
                x0 = Sum('x0'),
                x8 = Sum('x8'),
                xh = Sum('xh'),
                xp = Sum('xp')
            )
        Params_by_hour_list = list(Params_by_hour)        
        #   Суммирование мощности по фазам
        total_power = "{0:.3f}".format(sum([_['total_power'] for _ in Params_by_hour_list])/1000)#Суммирование и округление до третьего знака
        #Рассчёт экономии
<<<<<<< HEAD

=======
        XP = "{0:.3f}".format(sum([100-_['xp'] for _ in Params_by_hour_list])/1000) #Экономия в Квт*ч
        XP_percent = "{0:.3f}".format((float(XP)/float(total_power)*100) if total_power != 0 else 0)
>>>>>>> 1f7c6f990b1124b3ff408bdf3a6a779c138abc03
        #Подготовка данных для графика экономии
        for el in Params_by_hour_list:
            power_dict[str(el['data_date'].replace(tzinfo=None))] = "{0:.3}".format(100-(el['x0']/el['x8']*100))
        #Сбор данных напряжения и тока в таблицу
        #   Вход
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
    dev = Device.objects.get(pk = device)
    
    if request.method == 'POST':
       date_from = datetime.strptime(request.POST['date_pick'].split(' ~ ')[0], '%Y-%m-%d %H:%M')                
       date_to = datetime.strptime(request.POST['date_pick'].split(' ~ ')[1], '%Y-%m-%d %H:%M')        
    else:        
        date_to = CachingRecord.objects.filter(adapter_id__in = Device.objects.get(pk = device).adapters.all()).aggregate(
                            max_date=Max('record_time')
                        )['max_date']
        if date_to is None:
            return #TODO: Сообщение: "Нет данных"
        date_from = date_to - timedelta(days = 1) if date_to else None

    if date_to - date_from <= timedelta(hours=3):
        segmentation = 'minute'
    elif (date_to - date_from > timedelta(hours=3)) & (date_to - date_from <= timedelta(days=7)):  
        segmentation = 'hour'
    elif (date_to - date_from > timedelta(days=7)) & (date_to - date_from <= timedelta(weeks=14)):
        segmentation = 'day'
    elif (date_to - date_from > timedelta(weeks=14)) & (date_to - date_from <= timedelta(weeks=28*3)):
        segmentation = 'week'
    elif (date_to - date_from > timedelta(weeks=28*3)) & (date_to - date_from <= timedelta(weeks=28*15)):
        segmentation = 'month'
    else:
        segmentation = 'year'

    params = [('p_AU1','Вход. Напряжение фазы 1'),
              ('p_AI1','Вход. Ток фазы 1'),
              ('p_BU1','Вход. Напряжение фазы 2'),
              ('p_BI1','Вход. Ток фазы 2'),
              ('p_CU1','Вход. Напряжение фазы 3'),
              ('p_CI1','Вход. Ток фазы 3'),
              ('p_AU2','Выход. Напряжение фазы 1'),
              ('p_AI2','Выход. Ток фазы 1'),
              ('p_BU2','Выход. Напряжение фазы 2'),
              ('p_BI2','Выход. Ток фазы 2'),
              ('p_CU2','Выход. Напряжение фазы 3'),
              ('p_CI2','Выход. Ток фазы 3'),]
       
    data_query = CachingRecord.objects.filter(
                                            adapter_id__in=dev.adapters.all(), 
                                            record_time__gte=date_from, 
                                            record_time__lte=date_to,
                                            )\
                                .annotate(data_date=Trunc('record_time', segmentation, tzinfo=None))\
                                .values('data_date', 'adapter_id')\
                                .annotate(p_AU1 = Avg('p_AU1'),
                                            p_AI1 = Avg('p_AI1'),
                                            p_BU1 = Avg('p_BU1'),
                                            p_BI1 = Avg('p_BI1'),
                                            p_CU1 = Avg('p_CU1'),
                                            p_CI1 = Avg('p_CI1'),
                                            p_AU2 = Avg('p_AU2'),
                                            p_AI2 = Avg('p_AI2'),
                                            p_BU2 = Avg('p_BU2'),
                                            p_BI2 = Avg('p_BI2'),
                                            p_CU2 = Avg('p_CU2'),
                                            p_CI2 = Avg('p_CI2'))
    _data = defaultdict(list)
    for d in data_query.iterator(): 
        for p, name in params:
            _data[name].append({'y': float(d[p]), 'x': str(d['data_date'].replace(tzinfo=None))})
    for name, val in _data.items():
        data_dict[name] = json.dumps(val)
    #Старый вариант
    #_data_id_links = {}
    #parameters = AdapterParameters.objects.select_related('id_adapter').filter(
    #    Q(id_adapter__device=device) &
    #    (Q(parameter_name__icontains = 'Ток') | Q(parameter_name__icontains = 'Напряжение'))
    #)
    #for p in parameters:
    #    _data_id_links[p.id_parameter] = p.id_adapter.adapter_name, p.parameter_name
    #_data = defaultdict(list)
    #data_query = Data.objects.filter(
    #                        id_record__id_adapter__device=device, 
    #                        id_record__record_time__gte=date_from, 
    #                        id_record__record_time__lte=date_to,
    #                        id_parameter__in=parameters.values('id_parameter'))\
    #                    .annotate(data_date=Trunc('id_record__record_time', segmentation, tzinfo=None))\
    #                    .prefetch_related('id_record')\
    #                    .values('id_parameter', 'data_date', 'id_record__id_adapter')\
    #                    .annotate(measure_value=Avg('measure_value'))
    #for d in data_query.iterator(): 
    #    _data[d['id_parameter']].append({'y': float(d['measure_value']), 'x': d['data_date'].replace(tzinfo=None)})
    #t2 = time()
    #for k,v in _data.items():
    #    adapter_name, parameter_name = _data_id_links[k]
    #    data_dict[adapter_name][parameter_name] = json.dumps(v, default=myconverter)

    return render(
        request,
        'app/entrances.html',        
        {
            'data': dict(data_dict),           
            
            'device': device
        }
    )
