from django.db import models
from django.db.models.fields import IntegerField

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=0, max_value=31, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super(IntegerField, self).__init__(verbose_name=verbose_name, name=name, **kwargs)

    def set_min(self, value):
        self.min_value = value

    def set_max(self, value):
        self.max_value = value

    def formfield(self, **kwargs):
        defaults = {
            'min_value':self.min_value,
            'max_value':self.max_value
        }
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)