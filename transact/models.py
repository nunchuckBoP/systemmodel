from django.db import models
from django.contrib.auth.models import User
import transact.managers as managers
from datetime import datetime

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

    DATA_TYPE_CHOICES = [
        (0, 'PINCHART'),
        (1, 'PINCHART-SEQUENCE'),
        (2, 'DATA BLOCK')
    ]

    objects = managers.TransactionManager()
    created_on = models.DateTimeField(verbose_name="Created On", auto_now_add=True)
    completed_on = models.DateTimeField(verbose_name="Completed On", null=True, blank=True)
    function = models.IntegerField(choices=FUNCTION_CHOICES)
    data_type = models.IntegerField(choices=DATA_TYPE_CHOICES, default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    has_errors = models.BooleanField(default=False, verbose_name="Has Errors")
    data_object = models.JSONField(null=True, blank=True)
    errors = models.JSONField(null=True, blank=True)

    @property
    def is_complete(self):
        if self.completed_on is not None:
            return True
        else:
            return False

    def completed(self):
        """
            This method marks the transaction completed
            and saves
        """
        self.completed_on = datetime.now()
        self.save()

    def retry(self):
        """
            This method provides a means of retrying the transaction.
            It clears the completed_on
        """
        self.completed_on = None
        self.save()