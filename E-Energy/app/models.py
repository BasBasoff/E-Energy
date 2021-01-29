# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django import forms
from django.contrib.auth.models import User, AbstractBaseUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import uuid

class Actions(models.Model):
    id_action = models.AutoField(db_column='ID_ACTION', primary_key=True)  # Field name made lowercase.
    id_job = models.ForeignKey('Jobs', models.DO_NOTHING, db_column='ID_JOB')  # Field name made lowercase.
    id_device = models.ForeignKey('Devices', models.DO_NOTHING, db_column='ID_DEVICE', blank=True, null=True)  # Field name made lowercase.
    action_name = models.CharField(db_column='ACTION_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    action_type_id = models.IntegerField(db_column='ACTION_TYPE_ID', blank=True, null=True)  # Field name made lowercase.
    is_enabled = models.CharField(db_column='IS_ENABLED', max_length=1)  # Field name made lowercase.
    action_data = models.BinaryField(db_column='ACTION_DATA', blank=True, null=True)  # Field name made lowercase.
    action_order = models.SmallIntegerField(db_column='ACTION_ORDER')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'actions'
        unique_together = (('id_job', 'action_order'),)


class AdapterParameters(models.Model):
    id_parameter = models.AutoField(db_column='ID_PARAMETER', primary_key=True)  # Field name made lowercase.
    id_adapter = models.ForeignKey('Adapters', models.DO_NOTHING, db_column='ID_ADAPTER')  # Field name made lowercase.
    parameter_name = models.CharField(db_column='PARAMETER_NAME', max_length=99)  # Field name made lowercase.
    value_type = models.IntegerField(db_column='VALUE_TYPE')  # Field name made lowercase.
    param_type = models.IntegerField(db_column='PARAM_TYPE')  # Field name made lowercase.
    logical_id = models.SmallIntegerField(db_column='LOGICAL_ID')  # Field name made lowercase.
    parameter_order = models.SmallIntegerField(db_column='PARAMETER_ORDER')  # Field name made lowercase.
    mul_koeff = models.FloatField(db_column='MUL_KOEFF')  # Field name made lowercase.
    status_param = models.IntegerField(db_column='STATUS_PARAM')  # Field name made lowercase.
    id_measure = models.ForeignKey('ParamMeasures', models.DO_NOTHING, db_column='ID_MEASURE', blank=True, null=True)  # Field name made lowercase.
    overload_value = models.FloatField(db_column='OVERLOAD_VALUE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'adapter_parameters'
        unique_together = (('id_adapter', 'parameter_order'),)


class Adapters(models.Model):
    id_adapter = models.AutoField(db_column='ID_ADAPTER', primary_key=True)  # Field name made lowercase.
    id_device = models.ForeignKey('Devices', models.DO_NOTHING, db_column='ID_DEVICE')  # Field name made lowercase.
    adapter_name = models.CharField(db_column='ADAPTER_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    adapter_description = models.TextField(db_column='ADAPTER_DESCRIPTION', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    adapter_order = models.SmallIntegerField(db_column='ADAPTER_ORDER')  # Field name made lowercase.
    adapter_logical_id = models.SmallIntegerField(db_column='ADAPTER_LOGICAL_ID')  # Field name made lowercase.
    adapter_type_id = models.IntegerField(db_column='ADAPTER_TYPE_ID')  # Field name made lowercase.
    adapter_type_name = models.CharField(db_column='ADAPTER_TYPE_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'adapters'


class Computers(models.Model):
    id_computer = models.AutoField(db_column='ID_COMPUTER', primary_key=True)  # Field name made lowercase.
    name_computer = models.CharField(db_column='NAME_COMPUTER', max_length=50)  # Field name made lowercase.
    desc_computer = models.TextField(db_column='DESC_COMPUTER', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'computers'


class Data(models.Model):
    id_record = models.OneToOneField('Records', models.DO_NOTHING, db_column='ID_RECORD', primary_key=True)  # Field name made lowercase.
    id_parameter = models.IntegerField(db_column='ID_PARAMETER')  # Field name made lowercase.
    param_value = models.FloatField(db_column='PARAM_VALUE')  # Field name made lowercase.
    measure_value = models.FloatField(db_column='MEASURE_VALUE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'data'
        unique_together = (('id_record', 'id_parameter'),)



class DataCur(models.Model):
    id_adapter = models.OneToOneField('RecordsCur', models.DO_NOTHING, db_column='ID_ADAPTER', primary_key=True)  # Field name made lowercase.
    id_parameter = models.IntegerField(db_column='ID_PARAMETER')  # Field name made lowercase.
    param_value = models.FloatField(db_column='PARAM_VALUE')  # Field name made lowercase.
    measure_value = models.FloatField(db_column='MEASURE_VALUE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'data_cur'
        unique_together = (('id_adapter', 'id_parameter'),)


class DataOld(models.Model):
    id_record = models.IntegerField(db_column='ID_RECORD', primary_key=True)  # Field name made lowercase.
    id_parameter = models.IntegerField(db_column='ID_PARAMETER')  # Field name made lowercase.
    param_value = models.FloatField(db_column='PARAM_VALUE')  # Field name made lowercase.
    measure_value = models.FloatField(db_column='MEASURE_VALUE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'data_old'
        unique_together = (('id_record', 'id_parameter'),)


class Devices(models.Model):
    device_id = models.AutoField(db_column='DEVICE_ID', primary_key=True)  # Field name made lowercase.
    device_name = models.CharField(db_column='DEVICE_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    device_type = models.IntegerField(db_column='DEVICE_TYPE', blank=True, null=True)  # Field name made lowercase.
    device_type_name = models.CharField(db_column='DEVICE_TYPE_NAME', max_length=200)  # Field name made lowercase.
    device_clsid = models.CharField(db_column='DEVICE_CLSID', max_length=40)  # Field name made lowercase.
    device_description = models.TextField(db_column='DEVICE_DESCRIPTION', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    device_data = models.BinaryField(db_column='DEVICE_DATA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'devices'


class Groups(models.Model):
    id_group = models.AutoField(db_column='ID_GROUP', primary_key=True)  # Field name made lowercase.
    id_owner = models.SmallIntegerField(db_column='ID_OWNER', blank=True, null=True)  # Field name made lowercase.
    group_name = models.CharField(db_column='GROUP_NAME', max_length=200)  # Field name made lowercase.
    group_type = models.IntegerField(db_column='GROUP_TYPE')  # Field name made lowercase.
    group_order = models.SmallIntegerField(db_column='GROUP_ORDER')  # Field name made lowercase.
    device = models.ForeignKey(Devices, models.DO_NOTHING, db_column='DEVICE_ID', blank=True, null=True)  # Field name made lowercase.
    group_options = models.TextField(db_column='GROUP_OPTIONS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    group_description = models.TextField(db_column='GROUP_DESCRIPTION', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'groups'
        unique_together = (('id_owner', 'group_order'),)


class Jobs(models.Model):
    id_job = models.AutoField(db_column='ID_JOB', primary_key=True)  # Field name made lowercase.
    job_name = models.CharField(db_column='JOB_NAME', max_length=100)  # Field name made lowercase.
    is_enabled = models.CharField(db_column='IS_ENABLED', max_length=1)  # Field name made lowercase.
    start_mode = models.IntegerField(db_column='START_MODE')  # Field name made lowercase.
    start_time = models.DateTimeField(db_column='START_TIME')  # Field name made lowercase.
    offset_time = models.DateTimeField(db_column='OFFSET_TIME')  # Field name made lowercase.
    max_exec_time = models.DateTimeField(db_column='MAX_EXEC_TIME')  # Field name made lowercase.
    job_option = models.BinaryField(db_column='JOB_OPTION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jobs'


class Log(models.Model):
    id_log = models.AutoField(db_column='ID_LOG', primary_key=True)  # Field name made lowercase.
    id_session = models.ForeignKey('Sessions', models.DO_NOTHING, db_column='ID_SESSION')  # Field name made lowercase.
    date_time = models.DateTimeField(db_column='DATE_TIME')  # Field name made lowercase.
    id_device = models.ForeignKey(Devices, models.DO_NOTHING, db_column='ID_DEVICE', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    message = models.CharField(db_column='MESSAGE', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'log'


class ParamMeasures(models.Model):
    id_measure = models.AutoField(db_column='ID_MEASURE', primary_key=True)  # Field name made lowercase.
    measure_type = models.SmallIntegerField(db_column='MEASURE_TYPE')  # Field name made lowercase.
    measure_num = models.SmallIntegerField(db_column='MEASURE_NUM')  # Field name made lowercase.
    measure_name = models.CharField(db_column='MEASURE_NAME', max_length=50)  # Field name made lowercase.
    koeff = models.FloatField(db_column='KOEFF')  # Field name made lowercase.
    is_multiplier = models.CharField(db_column='IS_MULTIPLIER', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'param_measures'
        unique_together = (('measure_type', 'measure_num'),)


class Records(models.Model):
    id_record = models.AutoField(db_column='ID_RECORD', primary_key=True)  # Field name made lowercase.
    id_adapter = models.ForeignKey(Adapters, models.DO_NOTHING, db_column='ID_ADAPTER')  # Field name made lowercase.
    record_time = models.DateTimeField(db_column='RECORD_TIME')  # Field name made lowercase.
    status = models.IntegerField(db_column='STATUS')  # Field name made lowercase.
    record_index = models.IntegerField(db_column='RECORD_INDEX')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'records'
        unique_together = (('id_adapter', 'record_time', 'record_index', 'id_record'),)


class RecordsCur(models.Model):
    id_adapter = models.OneToOneField(Adapters, models.DO_NOTHING, db_column='ID_ADAPTER', primary_key=True)  # Field name made lowercase.
    record_time = models.DateTimeField(db_column='RECORD_TIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'records_cur'


class RecordsOld(models.Model):
    id_record = models.AutoField(db_column='ID_RECORD', primary_key=True)  # Field name made lowercase.
    id_adapter = models.ForeignKey(Adapters, models.DO_NOTHING, db_column='ID_ADAPTER')  # Field name made lowercase.
    record_time = models.DateTimeField(db_column='RECORD_TIME')  # Field name made lowercase.
    status = models.IntegerField(db_column='STATUS')  # Field name made lowercase.
    record_index = models.IntegerField(db_column='RECORD_INDEX')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'records_old'
        unique_together = (('id_adapter', 'record_time', 'record_index', 'id_record'),)


class Sessions(models.Model):
    id_session = models.AutoField(db_column='ID_SESSION', primary_key=True)  # Field name made lowercase.
    id_computer = models.ForeignKey(Computers, models.DO_NOTHING, db_column='ID_COMPUTER')  # Field name made lowercase.
    id_user = models.SmallIntegerField(db_column='ID_USER', blank=True, null=True)  # Field name made lowercase.
    start_session = models.DateTimeField(db_column='START_SESSION')  # Field name made lowercase.
    finish_session = models.DateTimeField(db_column='FINISH_SESSION', blank=True, null=True)  # Field name made lowercase.
    prog_title = models.CharField(db_column='PROG_TITLE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sessions'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)


class Users(models.Model):
    id_user = models.AutoField(db_column='ID_USER', primary_key=True)  # Field name made lowercase.
    user_login = models.CharField(db_column='USER_LOGIN', unique=True, max_length=30)  # Field name made lowercase.
    user_password = models.CharField(db_column='USER_PASSWORD', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_role = models.IntegerField(db_column='USER_ROLE')  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    user_description = models.TextField(db_column='USER_DESCRIPTION', blank=True, null=True)  # Field name made lowercase. This field type is a guess

    class Meta:
        managed = False
        db_table = 'users'


class Versions(models.Model):
    id_version = models.AutoField(db_column='ID_VERSION', primary_key=True)  # Field name made lowercase.
    ver = models.FloatField(db_column='VER', blank=True, null=True)  # Field name made lowercase.
    ver_date = models.DateTimeField(db_column='VER_DATE', blank=True, null=True)  # Field name made lowercase.
    changes = models.TextField(db_column='CHANGES', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'versions'

class Profile(AbstractBaseUser, models.Model):
    id_pk = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    u_login = models.CharField(unique=True, max_length=30, default='_Login_is_not_provided')
    u_password = models.CharField(max_length=100, blank=True, null=True, default='')
    u_role = models.IntegerField(default='2')
    u_name = models.CharField(max_length=150, blank=True, null=True)
    user_id = models.OneToOneField(Users, null=True, on_delete = models.CASCADE)
    user_auth = models.OneToOneField(User, on_delete=models.CASCADE)
    id_device = models.ManyToManyField(Devices, null=True)
    
    def save(self, *args, **kwargs):
        if not User.objects.filter(username = self.u_login).exists():
            user_auth = User.objects.create_user(username=self.u_login)
            user_auth.set_password(u_password)
            user_auth.save()
            users = Users(user_login=self.u_login, user_password=self.u_password, user_role=self.u_role, user_name=self.u_name)
            users.save()
        else:
            user_auth = User.objects.get(username = self.u_login)
            users = Users.objects.get(user_login = self.u_login)
        self.user_auth_id = user_auth.id
        self.user_id_id = users.id_user
        super(Profile, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):       
        self.user_auth_id.delete()
        self.user_id_id.delete()
        super(Profile, self).delete(*args, **kwargs)
