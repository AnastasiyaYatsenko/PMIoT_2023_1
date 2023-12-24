from django import forms
# from pmiot.models import Measurement

# class MeasurementForm(forms.ModelForm):
#     class Meta:
#         model = Measurement
#         fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=120,
                               widget=forms.PasswordInput)

        