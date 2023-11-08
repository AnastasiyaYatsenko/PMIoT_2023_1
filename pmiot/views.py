from datetime import datetime
import os
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.conf import settings

from pmiot.models import Measurement
from pmiot.forms import MeasurementForm
from pmiot.forms import ChangeValueForm

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

# class MeasurementCreate(generic.CreateView):
#     form_class = MeasurementForm
#     template_name = 'pmiot/create_measurement.html'
#     success_url = reverse_lazy('measurement_list')

class MeasurementDetails(generic.DetailView, generic.edit.FormMixin):
    model = Measurement
    context_object_name = 'details'
    form_class = ChangeValueForm
    template_name = 'pmiot/measurement_details.html'
    
    def get_success_url(self):
        return reverse('measurement_details', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(MeasurementDetails, self).get_context_data(**kwargs)
        context['form'] = ChangeValueForm(initial={'post': self.object})
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        form.save()
        return super(MeasurementDetails, self).form_valid(form)

def about(request):
    return render(
        request,
        'pmiot/about.html'
    )
