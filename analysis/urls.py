from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inside/', views.InsideView.as_view(), name='inside'),
    path('inside/exposure/pc/', views.ExposurePC.as_view(), name='exppc'),
]