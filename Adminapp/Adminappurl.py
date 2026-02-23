from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('districtreg/', views.districtreg, name='districtreg'),
    path('deletedistrict/<id>', views.deletedistrict, name='deletedistrict'),
    path('editdistrict/<id>', views.editdistrict, name='editdistrict'),
    path('locationreg/', views.locationreg, name='locationreg'),
    path('editlocation/<id>', views.editlocation, name='editlocation'),
    path('deletelocation/<id>', views.deletelocation, name='deletelocation'),
    path('categoryreg/', views.categoryreg, name='categoryreg'),
    path('editcategory/<id>', views.editcategory, name='editcategory'),
    path('deletecategory/<id>', views.deletecategory, name='deletecategory'),
    path('timereg/', views.timereg, name='timereg'),
    path('edittime/<id>', views.edittime, name='edittime'),
    path('sizereg/', views.sizereg, name='sizereg'),
    path('editsize/<id>', views.editsize, name='editsize'),
    path('deletesize/<id>', views.deletesize, name='deletesize'),
    path('verification/', views.verification, name='verification'),
    path('accept/<id>', views.accept, name='accept'),
    path('reject/<id>', views.reject, name='reject'),
    path('logout/', views.logout, name="logout"),
    path('ownerreport', views.ownerreport, name='ownerreport'),
    path('locationreport', views.locationreport, name='locationreport'),
    path('viewturfpayment/', views.viewturfpayment, name='viewturfpayment'),
    path('paymentexcel/', views.paymentexcel, name='paymentexcel'),

]
