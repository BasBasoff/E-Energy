from django.contrib import admin

from .models import Data
from .models import DevicesToUsers
from .models import Devices
from .models import Adapters
from .models import Records

admin.site.register(Data)
admin.site.register(DevicesToUsers)
admin.site.register(Devices)
admin.site.register(Adapters)
admin.site.register(Records)