from django import forms
from pmiot.models import Measurement

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = '__all__'

class ChangeValueForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('value',)