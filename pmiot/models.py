from django.db import models


class Measurement(models.Model):
    isWorking = models.BooleanField(default=False)
    min_value = models.IntegerField(default=0)
    max_value = models.IntegerField(default=100)
    value = models.IntegerField(default=0)
    measurementName = models.CharField(default='name', max_length=250)
    measurementType = models.CharField(default='type', max_length=250)
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ['measurementName']

    def __unicode__(self):
        return self.value
