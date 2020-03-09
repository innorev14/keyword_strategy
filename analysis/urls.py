from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('trend/', views.Trend.as_view(), name='trend'),
    path('search/', views.Search.as_view(), name='search'),

]