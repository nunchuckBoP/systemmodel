from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class Device(models.Model):
    part_number = models.CharField(verbose_name="Part Number", unique=True, max_length=256)
    description = models.CharField(max_length=1024)
    has_io = models.BooleanField(verbose_name="Device has I/O or Data Points.", default=False)
    has_comms = models.BooleanField(verbose_name="Device Has Communication Port", default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.part_number + " " + self.description

class Chassis(Device):
    part_number = models.CharField(verbose_name="Part Number")
    description = models.CharField(max_length=1024)
    slot_limit = models.IntegerField(verbose_name="Slot Count", null=True, blank=True)
    history = HistoricalRecords()