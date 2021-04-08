from django.db import models

# Create your models here.

class Transaction(models.Model):
    
    STATUS_CHOICES = [
        (0, 'NOT STARTED'),
        (1, 'IN PROGRESS'),
        (2, 'ABORTED WITH ERRORS'),
        (3, 'COMPLETED WITH ERRORS'),
        (4, 'SUCCESS')
    ]
    created_on = models.DateTimeField(verbose_name="created on")
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    errors = models.JSONField()