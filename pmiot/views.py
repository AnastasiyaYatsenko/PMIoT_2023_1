from datetime import datetime
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.conf import settings
from django.contrib import messages

from pmiot.models import Measurement
from pmiot.forms import MeasurementForm
# from pmiot.forms import ChangeValueForm

# from django.http import HttpResponse

# Create your views here.


class MeasurementList(generic.ListView):
    model = Measurement
    context_object_name = 'measurements'
    template_name = 'measurement_list.html'

    def get(self, request, *args, **kwargs):
        # try:
        #     file_path = os.path.join(settings.BASE_DIR, 'test_data.txt')
        #     measurement_file = open(file_path, 'r')

        #     for value in measurement_file:
        #         Measurement.objects.get_or_create(value=value)

        # except IOError:
        #     pass

        return super(MeasurementList, self).get(request, *args, **kwargs)


class MeasurementCreate(generic.CreateView):
    form_class = MeasurementForm
    template_name = 'pmiot/create_measurement.html'
    success_url = reverse_lazy('measurement_list')

# show data about sensor
def measurement_details(request, measurement_id):
    # get sensor by id
    sensor = get_object_or_404(Measurement, pk=measurement_id)
    # pass to page
    context = {'details': sensor}
    return render(request, 'pmiot/measurement_details.html', context)

# change value for sensor
def change_value(request, measurement_id):
    # clear previous messages
    storage = messages.get_messages(request)
    # get sensor by id
    sensor = get_object_or_404(Measurement, pk=measurement_id)
    # get new value from form
    new_value = int(request.POST['enter_value'])
    # check if value is in borders
    if new_value >= sensor.min_value and new_value <= sensor.max_value:
        # change value in db
        sensor.value = new_value
        sensor.save()
    else:
        # prepare error message to show
        messages.error(request, 'Value should be between {} and {}! You entered {}!'.format(sensor.min_value, sensor.max_value, new_value))
    return HttpResponseRedirect(reverse('measurement_details',
                                        args=(measurement_id,)))

def about(request):
    return render(request, 'pmiot/about.html')