from django.template.defaulttags import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('ownerregistration/', views.ownerregistration, name='ownerregistration'),
    path('selectlocation/', views.selectlocation, name='selectlocation'),
    path('login/', views.login, name='login'),
    path('customerreg/', views.customerreg, name='customerreg'),

]
