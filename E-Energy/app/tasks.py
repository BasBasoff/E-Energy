from E_Energy.celeryapp import app
from .models import CachingData, Data, AdapterParameters, Records
from datetime import datetime
from django.forms.models import model_to_dict


def preparation_dict(instance):
    dict = model_to_dict(instance)
    dict['record_id'] = dict.pop('id_record')
    dict['parameter_id'] = dict.pop('id_parameter')
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
            CachingData.objects.create(
                record_time=record_instance.record_time,
                adapter_id=record_instance.id_adapter.id_adapter,
                **preparation_dict(data_instance)
            )

        # CachingData.objects.bulk_create(
        #     [
        #         CachingData(
        #             record_time=record_instance.record_time,
        #             adapter_id=record_instance.id_adapter,
        #             **preparation_dict(data_instance)
        #         ) for data_instance in new_data_instances
        #     ]
        # )
