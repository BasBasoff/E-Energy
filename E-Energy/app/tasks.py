from E_Energy.celeryapp import app
from .models import CachingData, Data, AdapterParameters, Records
from datetime import datetime


@app.task
def data_caching():
    try:
        last_caching_record = CachingData.objects.last().record
    except AttributeError:
        last_caching_record = Records(record_time=datetime(2000, 1,1,0,1))

    new_record_instances = Records.objects.filter(
        record_time__gt=last_caching_record.record_time
    )

    for record_instance in new_record_instances.iterator():
        new_data_instances = list(
            Data.objects.filter(id_record=record_instance.id_record)
        )

        CachingData.objects.bulk_create(
            [
                CachingData(
                    record_time=record_instance.record_time,
                    adapter_id=record_instance.id_adapter,
                    **data_instance
                ) for data_instance in new_data_instances
            ]
        )
