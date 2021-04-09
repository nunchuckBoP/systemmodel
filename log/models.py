from django.db import models
import log.managers as managers

LOGGING_LEVEL_DEBUG = 0
LOGGING_LEVEL_INFO = 1
LOGGING_LEVEL_ERROR = 2

# Create your models here.
class Entry(models.Model):

    LOGGING_LEVEL_CHOICES = [
        (LOGGING_LEVEL_DEBUG, 'DEBUG'),
        (LOGGING_LEVEL_INFO, 'INFO'),
        (LOGGING_LEVEL_ERROR, 'ERROR')
    ]

    objects = managers.EntryManager()
    time = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    @property
    def message_short(self):
        return self.message[0:120] + "..."
