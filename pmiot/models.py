from django.db import models


class Measurement(models.Model):
    measurementName = models.CharField(default='Name', max_length=250)
    measurementType = models.CharField(default='Type', max_length=250)
    description = models.CharField(max_length=250, blank=True, null=True)
    min_value = models.IntegerField(default=0)
    max_value = models.IntegerField(default=100)
    value = models.FloatField(default=0, blank=True, null=True)
    dimension = models.CharField(default='°C', max_length=10)
    isWorking = models.BooleanField(default=False)

    image = models.ImageField(default=None, upload_to='', null=True)

    class Meta:
        ordering = ['measurementName']

    def __unicode__(self):
        return self.value


class Archive(models.Model):
    sensor_id = models.ForeignKey(Measurement,on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    timestamp=models.DateTimeField(default=None)

    class Meta:
        ordering = ['timestamp']

    # def __unicode__(self):
    #     return self.value
