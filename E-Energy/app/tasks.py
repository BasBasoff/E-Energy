from E_Energy.celery import app
from Models import CachingData, Data, AdapterParameters, Records


@app.task
def data_caching():
    last_caching_record = CachingData.objects.last().record
    new_record_instances = Records.filter(
        record_time__gt=last_caching_record.record_time
    )

    for record_instance in new_record_instances.iterator():
        new_data_instances = list(
            Data.objects.filter(id_record=instance.id_record)
        )

        CachingData.objects.bulk_create(
            [
                Entry(
                    record_time=record_instance.record_time,
                    adapter_id=record_instance.id_adapter,
                    **data_instance
                ) for data_instance in new_data_instances
            ]
        )
