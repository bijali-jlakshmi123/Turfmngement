from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='customerhome'),
    path('searchturf/', views.searchturf, name='searchturf'),
    path('turfview/', views.turfview, name='turfview'),
    path('selectloc', views.selectloc, name='selectloc'),
    path('viewmore/<id>', views.viewmore, name='viewmore'),
    path('booking/<id>', views.booking, name='booking'),
    path('selecttime/', views.selecttime, name='selecttime'),
    path('payment/<id>', views.payment, name='payment'),
    path('logout', views.logout, name='logout'),
    path('mybookings/', views.mybookings, name='mybookings')
]
