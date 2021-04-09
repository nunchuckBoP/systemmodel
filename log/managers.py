from django.db import models
from log.models import LOGGING_LEVEL_DEBUG, LOGGING_LEVEL_ERROR, LOGGING_LEVEL_INFO

class EntryManager(models.manager):
    
    def add(self, level_string, message_string):
        l = level_string.lower().strip()
        if l == 'debug':
            level = LOGGING_LEVEL_DEBUG
        elif l == 'info':
            level = LOGGING_LEVEL_INFO
        elif l == 'error':
            level = LOGGING_LEVEL_ERROR
        else:
            raise ValueError()
            return None

        e = self.create(level, message_string)
        e.save()
