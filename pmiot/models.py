from django.db import models

# Create your models here.
class Measurement(models.Model):
    isWorking = models.BooleanField(default=False)
    value = models.IntegerField(max_length=50)
    measurementName = models.CharField(default='name', max_length=250)
    measurementType = models.CharField(default='type', max_length=250)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __unicode__(self):
        return self.value
