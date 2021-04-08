from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Transaction(models.Model):
    
    STATUS_CHOICES = [
        (0, 'NOT STARTED'),
        (1, 'IN PROGRESS'),
        (2, 'ABORTED WITH ERRORS'),
        (3, 'COMPLETED WITH ERRORS'),
        (4, 'SUCCESS')
    ]

    FUNCTION_CHOICES = [
        (0, 'DOWNLOAD'),
        (1, 'UPLOAD')
    ]
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    function = models.IntegerField(choices=FUNCTION_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    errors = models.JSONField()