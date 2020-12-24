"""
Definition of models.
"""
import uuid
from django.db import models
from django.db.models import CharField, DateTimeField, DecimalField, UUIDField

# Create your models here.
class EntranceMeasure(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = DateTimeField(auto_now = True)
    data = DecimalField(max_digits=10,decimal_places=3)
