from datetime import datetime
import pytz
import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.conf import settings
from django.contrib import messages

from pmiot.models import Measurement
from pmiot.forms import MeasurementForm, LoginForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from pmiot.scheduler.scheduler import process_data

KyivTz = pytz.timezone("Europe/Kiev")

class MeasurementList(LoginRequiredMixin, generic.ListView):
    model = Measurement
    context_object_name = 'measurements'
    template_name = 'measurement_list.html'
    login_url = "/login/"
    redirect_field_name = "login"

    def get(self, request, *args, **kwargs):
        # try:
        #     file_path = os.path.join(settings.BASE_DIR, 'test_data.txt')
        #     measurement_file = open(file_path, 'r')

        #     for value in measurement_file:
        #         Measurement.objects.get_or_create(value=value)

        # except IOError:
        #     pass

        return super(MeasurementList, self).get(request, *args, **kwargs)


class MeasurementCreate(LoginRequiredMixin, generic.CreateView):
    form_class = MeasurementForm
    template_name = 'pmiot/create_measurement.html'
    success_url = reverse_lazy('measurement_list')
    login_url = "/login/"
    redirect_field_name = "login"

# show data about sensor
@login_required(login_url="/login/")
def measurement_details(request, measurement_id):
    # update sensors
    process_data()
    # get sensor by id
    sensor = get_object_or_404(Measurement, pk=measurement_id)

    is_comfortable = (sensor.value > sensor.min_comfort) and (sensor.value < sensor.max_comfort)
    if ((not is_comfortable) and
            ((not sensor.is_notified) or
             (sensor.is_notified and ((datetime.now(KyivTz)-sensor.last_notified).total_seconds() > 30 ))))\
            and (sensor.need_notification and sensor.isWorking): #300
        msg = "Attention! The sensor value is "
        if sensor.value < sensor.min_comfort:
            msg += "lower than comfortable!"
        elif sensor.value > sensor.max_comfort:
            msg += "higher than comfortable!"
        sensor.is_notified = True
        sensor.last_notified = datetime.now(KyivTz)
        sensor.save()
        context = {'details': sensor,
                   'msg': msg}
        return render(request, 'pmiot/measurement_details.html', context)
    else:
        sensor.is_notified = False
    # pass to page
    context = {'details': sensor}
    return render(request, 'pmiot/measurement_details.html', context)

# change value for sensor
@login_required(login_url="/login/")
def change_value(request, measurement_id):
    # clear previous messages
    storage = messages.get_messages(request)
    # get sensor by id
    sensor = get_object_or_404(Measurement, pk=measurement_id)
    # get new value from form
    new_value = bool(request.POST['enter_value'])
    # check if value is in borders
    # if new_value >= sensor.min_value and new_value <= sensor.max_value:
    if new_value != sensor.isWorking:
        # change value in db
        sensor.isWorking = new_value
        sensor.save()
    else:
        # prepare error message to show
        messages.error(request, 'It is the same value. Curent value: {}'.format(sensor.isWorking))
    return HttpResponseRedirect(reverse('measurement_details',
                                        args=(measurement_id,)))

@login_required(login_url="/login/")
def about(request):
    return render(request, 'pmiot/about.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'pmiot/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'pmiot/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login')