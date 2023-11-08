from django.urls import path
from pmiot import views
from pmiot.views import MeasurementList
from pmiot.views import MeasurementCreate
from pmiot.views import MeasurementDetails

urlpatterns = [
    # path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path('', MeasurementList.as_view(), name="measurement_list"),
    path('measurement_details/<int:pk>', MeasurementDetails.as_view(), name='measurement_details'),
    path("create_measurement/", MeasurementCreate.as_view(),
         name="create_measurement"),
]
