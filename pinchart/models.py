from enum import unique
from django.db import models
from pinchart import managers
from django.db.models.fields import NullBooleanField
import numpy
import core.utils
from pinchart.fields import IntegerRangeField

# Create your models here.
class Pinchart(models.Model):
    objects = managers.PinchartManager()
    customer = models.IntegerField(default=0)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, blank=True, null=True)
    controller_ipaddress = models.GenericIPAddressField(verbose_name="Controller IP Address",
                                                        protocol='IPv4')
    controller_slot = models.IntegerField(verbose_name="Controller Slot #")

    def __str__(self):
        return self.name

    def __deep_copy__(self, new_name):
        n = core.utils.derive(self)
        n.name = new_name
        n.save()

    class Meta:
        unique_together = ("customer", "controller_ipaddress")

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
    objects = managers.WordManager()
    pinchart = models.ForeignKey(Pinchart, on_delete=models.CASCADE)
    group = models.CharField(max_length=82, blank=True, null=True)
    name = models.CharField(max_length=82) # word or variable name
    type = models.CharField(choices=TYPE_CHOICES, default='DINT', max_length=30)
    address_template = models.CharField(verbose_name="Address Template", max_length=1024)

    @property
    def bit_full(self):
        bit_descriptions = BitDescription.objects.filter(word=self)
        if len(bit_descriptions) >= 32 and self.type == '32-BIT' or \
            len(bit_descriptions) >= 16 and self.type == '16-BIT':
            return True
        else:
            return False
            
    @property
    def next_bit(self):
        if self.type == '32-BIT' or self.type == '16-BIT':
            return BitDescription.objects.get_next_available_bit(self)

    @property
    def has_children(self):
        if self.type == '32-BIT' or self.type == '16-BIT' and \
            len(BitDescription.objects.filter(word=self)) > 0:
                return True
        else:
            return False

    @property
    def bit_descriptions(self):
        if self.type == '16-BIT' or self.type == '32-BIT':
            return BitDescription.objects.filter(word=self)
        else:
            return False

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("pinchart", "name")

class BitDescription(models.Model):
    objects = managers.BitDescriptionManager()
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    bit = IntegerRangeField(verbose_name="Bit number 0-15, or 0-31", min_value=0, max_value=32)
    device = models.CharField(max_length=24, blank=True, null=True)
    description = models.CharField(max_length=1024)

    def __str__(self):
        if self.device is not None:
            device_string = self.device
        else:
            device_string = "None"
        return "Bit: %s Device: %s Description: %s" % (self.bit, device_string, self.description)

    class Meta:
        unique_together = ("word", "bit")

class Sequence(models.Model):
    objects = managers.SequenceManager()
    pinchart = models.ForeignKey(Pinchart, on_delete=models.CASCADE)
    name = models.CharField(max_length=82)
    number = models.IntegerField()
    address_template = models.CharField(max_length=1024, null=True, blank=True)
    name_address_template = models.CharField(max_length=1024, null=True, blank=True)
    locked = models.BooleanField(verbose_name="Locked for Editing", default=False)
    array_length = models.IntegerField(verbose_name="Step Count")

    @property
    def is_locked(self):
        if self.locked:
            return True
        else:
            return False

    @property
    def address(self):
        return self.address_template.replace(":sequence:", str(self.number))

    @property
    def name_address(self):
        return self.name_address_template.replace(":sequence:", str(self.number))

    def lock(self):
        self.locked = True
        self.save()

    def unlock(self):
        self.locked = False
        self.save()

    def __str__(self):
        return self.name

    def __deep_copy__(self, new_name):
        n = core.utils.derive(self)
        n.name = new_name
        n.save()

    class Meta:
        unique_together = ("pinchart", "number")

class Step(models.Model):
    objects = managers.StepManager()
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    description = models.CharField(max_length=82)

    def __str__(self):
        return self.description

    class Meta:
        unique_together = ("sequence", "number")

class StepData(models.Model):
    objects = managers.StepDataManager()
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.SET_NULL, null=True, blank=True)
    value_bool = models.BooleanField(default=False)
    value_dint = models.IntegerField(default=0, blank=True, null=True)
    value_real = models.DecimalField(default=0.0, blank=True, null=True, decimal_places=3, max_digits=10)
    value_string = models.CharField(default=None, blank=True, null=True, max_length=1024)
    value_int = models.IntegerField(default=0, null=True, blank=True)
    value_b0 = models.BooleanField(default=0, null=True, blank=True)
    value_b1 = models.BooleanField(default=0, null=True, blank=True)
    value_b2 = models.BooleanField(default=0, null=True, blank=True)
    value_b3 = models.BooleanField(default=0, null=True, blank=True)
    value_b4 = models.BooleanField(default=0, null=True, blank=True)
    value_b5 = models.BooleanField(default=0, null=True, blank=True)
    value_b6 = models.BooleanField(default=0, null=True, blank=True)
    value_b7 = models.BooleanField(default=0, null=True, blank=True)
    value_b8 = models.BooleanField(default=0, null=True, blank=True)
    value_b9 = models.BooleanField(default=0, null=True, blank=True)
    value_b10 = models.BooleanField(default=0, null=True, blank=True)
    value_b11 = models.BooleanField(default=0, null=True, blank=True)
    value_b12 = models.BooleanField(default=0, null=True, blank=True)
    value_b13 = models.BooleanField(default=0, null=True, blank=True)
    value_b14 = models.BooleanField(default=0, null=True, blank=True)
    value_b15 = models.BooleanField(default=0, null=True, blank=True)
    value_b16 = models.BooleanField(default=0, null=True, blank=True)
    value_b17 = models.BooleanField(default=0, null=True, blank=True)
    value_b18 = models.BooleanField(default=0, null=True, blank=True)
    value_b19 = models.BooleanField(default=0, null=True, blank=True)
    value_b20 = models.BooleanField(default=0, null=True, blank=True)
    value_b21 = models.BooleanField(default=0, null=True, blank=True)
    value_b22 = models.BooleanField(default=0, null=True, blank=True)
    value_b23 = models.BooleanField(default=0, null=True, blank=True)
    value_b24 = models.BooleanField(default=0, null=True, blank=True)
    value_b25 = models.BooleanField(default=0, null=True, blank=True)
    value_b26 = models.BooleanField(default=0, null=True, blank=True)
    value_b27 = models.BooleanField(default=0, null=True, blank=True)
    value_b28 = models.BooleanField(default=0, null=True, blank=True)
    value_b29 = models.BooleanField(default=0, null=True, blank=True)
    value_b30 = models.BooleanField(default=0, null=True, blank=True)
    value_b31 = models.BooleanField(default=0, null=True, blank=True)

    def set_value(self, value):
        
        # get the type
        _type = self.word.type

        if _type == 'BOOL':
            self.value_bool = value
        elif _type == 'DINT':
            self.value_dint = numpy.int32(value)
        elif _type == 'INT':
            self.value_int = numpy.int16(value)
        elif _type == 'REAL':
            self.value_real = float(value)
        elif _type == '32-BIT':
            # set the individual booleans
            pass
        elif _type == '16-BIT':
            # set the individual booleans
            pass
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
        if _type == 'DINT':
            return self.value_dint
        elif _type == '32-BIT':
            # puts the individual bits in a list of booleans
            bin_list = [
                self.value_b31, self.value_b30, self.value_b29, self.value_b28,
                self.value_b27, self.value_b26, self.value_b25, self.value_b24,
                self.value_b23, self.value_b22, self.value_b21, self.value_b20,
                self.value_b19, self.value_b18, self.value_b17, self.value_b16,
                self.value_b15, self.value_b14, self.value_b13, self.value_b12,
                self.value_b11, self.value_b10, self.value_b9,  self.value_b8,
                self.value_b7,  self.value_b6,  self.value_b5,  self.value_b4,
                self.value_b3,  self.value_b2,  self.value_b1,  self.value_b0
            ]

            # converts the list of booleans to ones and zeros
            bin_ints = [int(i) for i in bin_list]

            # takes the bits and coverts them to a value
            res = 0
            for ele in bin_ints:
                res = (res << 1) | ele
            return numpy.int32(res)

        elif _type == '16-BIT':            
            # puts the individual bits in a list of booleans
            bin_list = [
                self.value_b15, self.value_b14, self.value_b13, self.value_b12,
                self.value_b11, self.value_b10, self.value_b9,  self.value_b8,
                self.value_b7,  self.value_b6,  self.value_b5,  self.value_b4,
                self.value_b3,  self.value_b2,  self.value_b1,  self.value_b0
            ]

            # converts the list of booleans to ones and zeros
            bin_ints = [int(i) for i in bin_list]

            # takes the bits and coverts them to a value
            res = 0
            for ele in bin_ints:
                res = (res << 1) | ele
            return numpy.int16(res)

        elif _type == 'INT':
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
    def full_address(self):
        _a = self.sequence.address_template + self.word.address_template
        _a = _a.replace(':sequence_number:', str(self.sequence.number))
        _a = _a.replace(':step:', str(self.step.number))
        return _a

    def __str__(self):
        self.value_bool

    class Meta:
        unique_together = ("step", "word")
