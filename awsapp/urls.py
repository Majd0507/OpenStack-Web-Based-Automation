from django.urls import path

from . import views

app_name = 'aws'
urlpatterns = [
    #ex: /awsapp/
    path('', views.index, name='index'),

    #ex: /awsapp/5/
    path('details/<instance_id>/', views.details, name='details'),

    #ex: /awsapp/5/
    path('create/', views.create, name='create'),

    path('login/', views.login, name='login'),

    path('start/<instance_id>/', views.start_instance, name='start_instance'),
    path('stop/<instance_id>/', views.stop_instance, name='stop_instance'),
    path('createattachevol/<instance_id>/', views.createAtacheVolume, name='createAtacheVolume'),

    path('volumes/', views.listVolumes, name='volumes'),

    path('detatch/<instance_id>/<volume_id>', views.detatchVolume, name='detatch'),

    path('deletevolume/<volume_id>', views.deleteVolume, name='deletevolume'),
    path('detatchdeletevolume/<instance_id>/<volume_id>', views.detatchDeleteVolume, name='detachdeletevolume'),
]
