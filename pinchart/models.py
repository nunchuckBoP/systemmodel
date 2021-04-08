from enum import unique
from django.db import models
from django.db.models.fields import NullBooleanField
import numpy

# Create your models here.

class Pinchart(models.Model):
    customer = models.IntegerField(default=0)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, blank=True, null=True)
    controller_ipaddress = models.GenericIPAddressField(verbose_name="Controller IP Address",
                                                        protocol='IPv4')
    controller_slot = models.IntegerField(verbose_name="Controller Slot #")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("customer", "name")

class Word(models.Model):
    TYPE_CHOICES = [
        ('BOOL', 'BOOL'),
        ('32-BIT', '32-BIT'),
        ('DINT', 'DINT'),
        ('REAL', 'REAL'),
        ('STRING', 'STRING'),
        ('INT', 'INT'),
        ('16-BIT', '16-BIT'),
        ('STEP DESCRIPTION', 'STEP DESCRIPTION'),
    ]
    pinchart = models.ForeignKey(Pinchart, on_delete=models.CASCADE)
    name = models.CharField(max_length=82) # word or variable name
    type = models.CharField(choices=TYPE_CHOICES, default='DINT', max_length=30)
    address_template = models.CharField(verbose_name="Address Template", max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("pinchart", "name")

class BitDescription(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    bit = models.IntegerField(verbose_name="Bit number 0-15, or 0-31")
    device = models.CharField(max_length=24, blank=True, null=True)
    description = models.CharField(max_length=1024)

    def __str__(self):
        if self.device is not None:
            return str(self.bit) + "[" + str(self.device) + "]" + " " + self.description
        else:
            return str(self.bit) + " " + self.description

    class Meta:
        unique_together = ("word", "bit")

class Sequence(models.Model):
    pinchart = models.ForeignKey(Pinchart, on_delete=models.CASCADE)
    name = models.CharField(max_length=82)
    number = models.IntegerField()
    address_template = models.CharField(max_length=1024, null=True, blank=True)
    name_address_template = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("pinchart", "number")

class Step(models.Model):

    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.IntegerField(verbose_name="Step Number")
    description = models.CharField(max_length=1024, default="**Spare Step**")
    value_bool = models.BooleanField(default=False)
    value_dint = models.IntegerField(default=0, blank=True, null=True)
    value_real = models.DecimalField(default=0.0, blank=True, null=True, decimal_places=3, max_digits=10)
    value_string = models.CharField(default=None, blank=True, null=True, max_length=1024)
    value_int = models.IntegerField(default=0, null=True, blank=True)

    def set_value(self, value):
        
        # get the type
        _type = self.word.type

        if _type == 'BOOL':
            self.value_bool = value
        elif _type == '32-BIT' or _type == 'DINT':
            self.value_dint = numpy.int32(value)
        elif _type == '16-BIT' or _type == 'INT':
            self.value_int = numpy.int16(value)
        elif _type == 'REAL':
            self.value_real = float(value)
        else:
            raise ValueError()

    @property
    def value(self):

        # gets the type of the value
        _type = self.word.type

        # selects which value to return based
        # on the type
        if _type == 'BOOL':
            return self.value_bool
        elif _type == '32-BIT' or _type == 'DINT':
            return numpy.int32(self.value_dint)
        elif _type == '16-BIT' or _type == 'INT':
            return numpy.int16(self.value_int)
        elif _type == 'REAL':
            return self.value_real
        elif _type == 'STRING':
            return self.value_string
        elif _type == 'STEP DESCRIPTION':
            return self.description
        else:
            raise ValueError()       

    @property
    def bin_value(self):
        
        _type = self.word.type

        if _type == '32-BIT':
            return numpy.binary_repr(self.value, width=32)
        elif _type == '16-BIT':
            return numpy.binary_repr(self.value, width=16)

    @property
    def full_address(self):
        _a = self.sequence.address_template + self.word.address_template
        _a = _a.replace(':sequence_number:', str(self.sequence.number))
        _a = _a.replace(':step:', str(self.number))
        return _a

    class Meta:
        unique_together = ("sequence", "number", "word")
