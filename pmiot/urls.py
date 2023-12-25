from django.urls import path
from pmiot import views
from pmiot.views import MeasurementList
from pmiot.views import MeasurementCreate
# from pmiot.views import MeasurementDetails

urlpatterns = [
    # path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path('', MeasurementList.as_view(), name="measurement_list"),
    path('measurement_details/<str:measurement_id>/', views.measurement_details, name='measurement_details'),
    path('change_value/<str:measurement_id>/', views.change_value, name='change_value'),
    path("create_measurement/", MeasurementCreate.as_view(),
         name="create_measurement"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
