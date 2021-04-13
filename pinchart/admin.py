from django.contrib import admin
import pinchart.models as models

# Register your models here.
class PinchartAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Pinchart, PinchartAdmin)

class WordAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Word, WordAdmin)

class SequenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Sequence, SequenceAdmin)

class StepAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Step, StepAdmin)

class StepDataAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.StepData, StepDataAdmin)