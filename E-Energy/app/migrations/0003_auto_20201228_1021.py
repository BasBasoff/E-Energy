# Generated by Django 3.1.4 on 2020-12-28 03:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201224_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id_action', models.AutoField(db_column='ID_ACTION', primary_key=True, serialize=False)),
                ('action_name', models.CharField(blank=True, db_column='ACTION_NAME', max_length=100, null=True)),
                ('action_type_id', models.IntegerField(blank=True, db_column='ACTION_TYPE_ID', null=True)),
                ('is_enabled', models.CharField(db_column='IS_ENABLED', max_length=1)),
                ('action_data', models.BinaryField(blank=True, db_column='ACTION_DATA', null=True)),
                ('action_order', models.SmallIntegerField(db_column='ACTION_ORDER')),
            ],
            options={
                'db_table': 'actions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AdapterParameters',
            fields=[
                ('id_parameter', models.AutoField(db_column='ID_PARAMETER', primary_key=True, serialize=False)),
                ('parameter_name', models.CharField(db_column='PARAMETER_NAME', max_length=99)),
                ('value_type', models.IntegerField(db_column='VALUE_TYPE')),
                ('param_type', models.IntegerField(db_column='PARAM_TYPE')),
                ('logical_id', models.SmallIntegerField(db_column='LOGICAL_ID')),
                ('parameter_order', models.SmallIntegerField(db_column='PARAMETER_ORDER')),
                ('mul_koeff', models.FloatField(db_column='MUL_KOEFF')),
                ('status_param', models.IntegerField(db_column='STATUS_PARAM')),
                ('overload_value', models.FloatField(db_column='OVERLOAD_VALUE')),
            ],
            options={
                'db_table': 'adapter_parameters',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Adapters',
            fields=[
                ('id_adapter', models.AutoField(db_column='ID_ADAPTER', primary_key=True, serialize=False)),
                ('adapter_name', models.CharField(blank=True, db_column='ADAPTER_NAME', max_length=150, null=True)),
                ('adapter_description', models.TextField(blank=True, db_column='ADAPTER_DESCRIPTION', null=True)),
                ('adapter_order', models.SmallIntegerField(db_column='ADAPTER_ORDER')),
                ('adapter_logical_id', models.SmallIntegerField(db_column='ADAPTER_LOGICAL_ID')),
                ('adapter_type_id', models.IntegerField(db_column='ADAPTER_TYPE_ID')),
                ('adapter_type_name', models.CharField(blank=True, db_column='ADAPTER_TYPE_NAME', max_length=150, null=True)),
            ],
            options={
                'db_table': 'adapters',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Computers',
            fields=[
                ('id_computer', models.AutoField(db_column='ID_COMPUTER', primary_key=True, serialize=False)),
                ('name_computer', models.CharField(db_column='NAME_COMPUTER', max_length=50)),
                ('desc_computer', models.TextField(blank=True, db_column='DESC_COMPUTER', null=True)),
            ],
            options={
                'db_table': 'computers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DataOld',
            fields=[
                ('id_record', models.IntegerField(db_column='ID_RECORD', primary_key=True, serialize=False)),
                ('id_parameter', models.IntegerField(db_column='ID_PARAMETER')),
                ('param_value', models.FloatField(db_column='PARAM_VALUE')),
                ('measure_value', models.FloatField(db_column='MEASURE_VALUE')),
            ],
            options={
                'db_table': 'data_old',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('device_id', models.AutoField(db_column='DEVICE_ID', primary_key=True, serialize=False)),
                ('device_name', models.CharField(blank=True, db_column='DEVICE_NAME', max_length=200, null=True)),
                ('device_type', models.IntegerField(blank=True, db_column='DEVICE_TYPE', null=True)),
                ('device_type_name', models.CharField(db_column='DEVICE_TYPE_NAME', max_length=200)),
                ('device_clsid', models.CharField(db_column='DEVICE_CLSID', max_length=40)),
                ('device_description', models.TextField(blank=True, db_column='DEVICE_DESCRIPTION', null=True)),
                ('device_data', models.BinaryField(blank=True, db_column='DEVICE_DATA', null=True)),
            ],
            options={
                'db_table': 'devices',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id_group', models.AutoField(db_column='ID_GROUP', primary_key=True, serialize=False)),
                ('id_owner', models.SmallIntegerField(blank=True, db_column='ID_OWNER', null=True)),
                ('group_name', models.CharField(db_column='GROUP_NAME', max_length=200)),
                ('group_type', models.IntegerField(db_column='GROUP_TYPE')),
                ('group_order', models.SmallIntegerField(db_column='GROUP_ORDER')),
                ('group_options', models.TextField(blank=True, db_column='GROUP_OPTIONS', null=True)),
                ('group_description', models.TextField(blank=True, db_column='GROUP_DESCRIPTION', null=True)),
            ],
            options={
                'db_table': 'groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id_job', models.AutoField(db_column='ID_JOB', primary_key=True, serialize=False)),
                ('job_name', models.CharField(db_column='JOB_NAME', max_length=100)),
                ('is_enabled', models.CharField(db_column='IS_ENABLED', max_length=1)),
                ('start_mode', models.IntegerField(db_column='START_MODE')),
                ('start_time', models.DateTimeField(db_column='START_TIME')),
                ('offset_time', models.DateTimeField(db_column='OFFSET_TIME')),
                ('max_exec_time', models.DateTimeField(db_column='MAX_EXEC_TIME')),
                ('job_option', models.BinaryField(blank=True, db_column='JOB_OPTION', null=True)),
            ],
            options={
                'db_table': 'jobs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id_log', models.AutoField(db_column='ID_LOG', primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField(db_column='DATE_TIME')),
                ('status', models.IntegerField(blank=True, db_column='STATUS', null=True)),
                ('message', models.CharField(blank=True, db_column='MESSAGE', max_length=300, null=True)),
            ],
            options={
                'db_table': 'log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ParamMeasures',
            fields=[
                ('id_measure', models.AutoField(db_column='ID_MEASURE', primary_key=True, serialize=False)),
                ('measure_type', models.SmallIntegerField(db_column='MEASURE_TYPE')),
                ('measure_num', models.SmallIntegerField(db_column='MEASURE_NUM')),
                ('measure_name', models.CharField(db_column='MEASURE_NAME', max_length=50)),
                ('koeff', models.FloatField(db_column='KOEFF')),
                ('is_multiplier', models.CharField(db_column='IS_MULTIPLIER', max_length=1)),
            ],
            options={
                'db_table': 'param_measures',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id_record', models.AutoField(db_column='ID_RECORD', primary_key=True, serialize=False)),
                ('record_time', models.DateTimeField(db_column='RECORD_TIME')),
                ('status', models.IntegerField(db_column='STATUS')),
                ('record_index', models.IntegerField(db_column='RECORD_INDEX')),
            ],
            options={
                'db_table': 'records',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RecordsOld',
            fields=[
                ('id_record', models.AutoField(db_column='ID_RECORD', primary_key=True, serialize=False)),
                ('record_time', models.DateTimeField(db_column='RECORD_TIME')),
                ('status', models.IntegerField(db_column='STATUS')),
                ('record_index', models.IntegerField(db_column='RECORD_INDEX')),
            ],
            options={
                'db_table': 'records_old',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('id_session', models.AutoField(db_column='ID_SESSION', primary_key=True, serialize=False)),
                ('id_user', models.SmallIntegerField(blank=True, db_column='ID_USER', null=True)),
                ('start_session', models.DateTimeField(db_column='START_SESSION')),
                ('finish_session', models.DateTimeField(blank=True, db_column='FINISH_SESSION', null=True)),
                ('prog_title', models.CharField(blank=True, db_column='PROG_TITLE', max_length=100, null=True)),
                ('active', models.CharField(db_column='Active', max_length=1)),
            ],
            options={
                'db_table': 'sessions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sysdiagrams',
            fields=[
                ('name', models.CharField(max_length=128)),
                ('principal_id', models.IntegerField()),
                ('diagram_id', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.IntegerField(blank=True, null=True)),
                ('definition', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sysdiagrams',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id_user', models.AutoField(db_column='ID_USER', primary_key=True, serialize=False)),
                ('user_login', models.CharField(db_column='USER_LOGIN', max_length=30, unique=True)),
                ('user_password', models.CharField(blank=True, db_column='USER_PASSWORD', max_length=30, null=True)),
                ('user_role', models.IntegerField(db_column='USER_ROLE')),
                ('user_name', models.CharField(blank=True, db_column='USER_NAME', max_length=150, null=True)),
                ('user_description', models.TextField(blank=True, db_column='USER_DESCRIPTION', null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Versions',
            fields=[
                ('id_version', models.AutoField(db_column='ID_VERSION', primary_key=True, serialize=False)),
                ('ver', models.FloatField(blank=True, db_column='VER', null=True)),
                ('ver_date', models.DateTimeField(blank=True, db_column='VER_DATE', null=True)),
                ('changes', models.TextField(blank=True, db_column='CHANGES', null=True)),
            ],
            options={
                'db_table': 'versions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DevicesToUsers',
            fields=[
                ('id_pk', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id_device', models.ManyToManyField(to='app.Devices')),
                ('id_user', models.ManyToManyField(to='app.Users')),
            ],
        ),
        migrations.DeleteModel(
            name='EntranceMeasure',
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id_record', models.OneToOneField(db_column='ID_RECORD', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.records')),
                ('id_parameter', models.IntegerField(db_column='ID_PARAMETER')),
                ('param_value', models.FloatField(db_column='PARAM_VALUE')),
                ('measure_value', models.FloatField(db_column='MEASURE_VALUE')),
            ],
            options={
                'db_table': 'data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RecordsCur',
            fields=[
                ('id_adapter', models.OneToOneField(db_column='ID_ADAPTER', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.adapters')),
                ('record_time', models.DateTimeField(db_column='RECORD_TIME')),
            ],
            options={
                'db_table': 'records_cur',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DataCur',
            fields=[
                ('id_adapter', models.OneToOneField(db_column='ID_ADAPTER', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.recordscur')),
                ('id_parameter', models.IntegerField(db_column='ID_PARAMETER')),
                ('param_value', models.FloatField(db_column='PARAM_VALUE')),
                ('measure_value', models.FloatField(db_column='MEASURE_VALUE')),
            ],
            options={
                'db_table': 'data_cur',
                'managed': False,
            },
        ),
    ]
