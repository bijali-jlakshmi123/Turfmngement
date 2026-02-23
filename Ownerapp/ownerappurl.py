from django.urls import path
from . import views
from .views import ExportExcel

urlpatterns = [
    path('home/', views.home, name='home1'),
    path('turfregistration/', views.turfregistration, name='turfregistration'),
    path('turftimereg/<id>', views.turftimereg, name='turftimereg'),
    path('viewturf/', views.viewturf, name='viewturf'),
    path('viewbookings/<id>', views.viewbookings, name='viewbookings'),
    path('logout', views.logout, name='logout'),
    path('bookingpiechart', views.bookingpiechart, name='bookingpiechart'),
    path('BookingExcel', views.BookingExcel, name='BookingExcel'),
    path('export_excel/', ExportExcel.as_view(), name='export_excel'),
    path('turfpayment/', views.turfpayment, name='turfpayment')

]
