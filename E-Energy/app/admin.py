from django.contrib import admin
from django.contrib.auth.models import User

from .models import Data
from .models import Profile
from .models import Devices
from .models import Adapters
from .models import Records
from .models import Users
from .models import Device
from .models import CachingData

@admin.register(Profile)
class Profile(admin.ModelAdmin):
	fields = ('u_login', 'u_password', 'u_role', 'u_name', 'id_device')

admin.site.register(Data)
admin.site.register(Devices)
admin.site.register(Adapters)
admin.site.register(Records)
admin.site.register(Users)
admin.site.register(CachingData)
@admin.register(Device)
class Device(admin.ModelAdmin):
	fields = ('name', 'adapters', 'devices')
