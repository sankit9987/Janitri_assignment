from django.urls import path
from .views import (
    PatientListCreateView,
    PatientRetrieveView,
    HeartRateCreateView,
    HeartRateListView,
)

urlpatterns = [
    path('patients/', PatientListCreateView.as_view(), name='patients-list-create'),
    path('patients/<int:pk>/', PatientRetrieveView.as_view(), name='patient-detail'),
    path('heart-rate/', HeartRateCreateView.as_view(), name='heartrate-create'),
    path('heart-rate/list/', HeartRateListView.as_view(), name='heartrate-list'),
]
