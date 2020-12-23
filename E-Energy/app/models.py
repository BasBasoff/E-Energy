"""
Definition of models.
"""
import uuid
from django.db import models
from django.db.models import CharField, DateTimeField, DecimalField, UUIDField

# Create your models here.
class EntranceMeasure(models.Model):
    EntranceID = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Date = DateTimeField(auto_now = True)
    Data = DecimalField(max_digits=10,decimal_places=3)
