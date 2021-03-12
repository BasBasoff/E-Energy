from E_Energy.celeryapp import app
from .models import CachingData, Data, AdapterParameters, Records, CachingRecord
from datetime import datetime
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist


def preparation_dict(instance):
    dict = model_to_dict(instance)
    dict['record_id'] = dict.pop('id_record')
    dict['adapter_id'] = dict.pop('id_adapter_id')
    return dict

def preparation_record_dict(instance):
    dict = model_to_dict(instance)
    dict['record_id'] = dict.pop('id_record')
    dict['adapter_id'] = dict.pop('id_adapter')
    return dict

@app.task(time_limit=115)
def data_caching():
    #try:
    last_record_id = CachingData.objects.latest('record_time').record_id
    print(last_record_id)
    print(CachingData.objects.latest('record_time').record_time)
    last_caching_record = Records.objects.get(id_record = last_record_id )
    print(last_caching_record.record_time)
    #except AttributeError:
    #    last_caching_record = Records(record_time=datetime(2020, 1,26,0,1))

    new_record_instances = Records.objects.filter(
        record_time__gt=last_caching_record.record_time
    ).order_by('record_time')

    for record_instance in new_record_instances.iterator(chunk_size=50):
        new_data_instances = list(
            Data.objects.filter(id_record=record_instance.id_record)
        )
        print(record_instance.id_record)
        print(record_instance.record_time)


        for data_instance in new_data_instances:
            Data.objects.create(
                record_time=record_instance.record_time,
                adapter_id=record_instance.id_adapter.id_adapter,
                **preparation_dict(data_instance)
            )

@app.task(time_limit=115)
def records_caching():
    try:
        last_record_id = CachingRecord.objects.latest('record_time').record_id
        print(last_record_id)
        print(CachingRecord.objects.latest('record_time').record_time)
        last_caching_record = Records.objects.get(id_record = last_record_id )
        print(last_caching_record.record_time)

    except (AttributeError, ObjectDoesNotExist):
       last_caching_record = Records(record_time=datetime(2020, 1,26,0,1))

    new_input_records = Records.objects.filter(
        record_time__gt=last_caching_record.record_time,
        id_adapter__adapter_name__icontains='вход'
    ).order_by('record_time')

    for input_record in new_input_records.iterator(chunk_size=200):
        input_datas = list(
            Data.objects.filter(id_record=input_record.id_record)
        )
        input_params = AdapterParameters.objects.filter(
            id_adapter = input_record.id_adapter_id)

        try:

            output_record = Records.objects.get(
                id_adapter__adapter_name__icontains='выход',
                id_adapter__device__in=input_record.id_adapter.device_set.all(),
                record_time=input_record.record_time
            )

            output_datas = list(
                Data.objects.filter(id_record=output_record.id_record)
            )

            output_params = AdapterParameters.objects.filter(
                id_adapter = output_record.id_adapter_id)

        except ObjectDoesNotExist:
            output_record = Records()
            output_datas = []
            output_params = []

        p_AU1 = next(
            (data.measure_value for data in input_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in input_params \
                        if 'Напряжение фазы 1' in p.parameter_name),
                    0)),
            0)
        p_BU1 = next(
            (data.measure_value for data in input_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in input_params \
                        if 'Напряжение фазы 2' in p.parameter_name),
                    0)),
            0)
        p_CU1 = next(
            (data.measure_value for data in input_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in input_params \
                        if 'Напряжение фазы 3' in p.parameter_name),
                    0)),
            0)
        p_AI1 = next(
            (data.measure_value for data in input_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in input_params \
                        if 'Ток фазы 1' in p.parameter_name),
                    0)),
            0)
        p_BI1 = next(
            (data.measure_value for data in input_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in input_params \
                        if 'Ток фазы 2' in p.parameter_name),
                    0)),
            0)
        p_CI1 = next(
            (data.measure_value for data in input_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in input_params \
                        if 'Ток фазы 3' in p.parameter_name),
                    0)),
            0)
        p_AU2 = next(
            (data.measure_value for data in output_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in output_params \
                        if 'Напряжение фазы 1' in p.parameter_name),
                    0)),
            0)
        p_BU2 = next(
            (data.measure_value for data in output_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in output_params \
                        if 'Напряжение фазы 2' in p.parameter_name),
                    0)),
            0)
        p_CU2 = next(
            (data.measure_value for data in output_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in output_params \
                        if 'Напряжение фазы 3' in p.parameter_name),
                    0)),
            0)
        p_AI2 = next(
            (data.measure_value for data in output_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in output_params \
                        if 'Ток фазы 1' in p.parameter_name),
                    0)),
            0)
        p_BI2 = next(
            (data.measure_value for data in output_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in output_params \
                        if 'Ток фазы 2' in p.parameter_name),
                    0)),
            0)
        p_CI2 = next(
            (data.measure_value for data in output_datas \
                if data.id_parameter==next(
                    (p.id_parameter for p in output_params \
                        if 'Ток фазы 3' in p.parameter_name),
                    0)),
            0)

        total_power = (p_AU1*p_AI1 + p_BU1*p_BI1 + p_CU1*p_CI1)/60

        x1 = p_AI1*p_AU2/60
        x2 = p_AI2*p_AU1/60
        x3 = p_BI1*p_BU2/60
        x4 = p_BI2*p_BU1/60
        x5 = p_CI1*p_CU2/60
        x6 = p_CI2*p_CU1/60
        x0 = x1+x3+x5
        x8 = x2+x4+x6
        xh = x0/x8*100 if x8 !=0 else 0
        xp = 100-xh



        CachingRecord.objects.create(
            p_AU1=p_AU1,
            p_BU1=p_BU1,
            p_CU1=p_CU1,
            p_AI1=p_AI1,
            p_BI1=p_BI1,
            p_CI1=p_CI1,

            p_AU2=p_AU2,
            p_BU2=p_BU2,
            p_CU2=p_CU2,
            p_AI2=p_AI2,
            p_BI2=p_BI2,
            p_CI2=p_CI2,

            total_power=total_power,

            x1=x1,
            x2=x2,
            x3=x3,
            x4=x4,
            x5=x5,
            x6=x6,
            x0=x0,
            x8=x8,
            xh=xh,
            xp=xp,
            **preparation_record_dict(input_record)
        )
        print(input_record.record_time)
