from django.db import models

from Adminapp.models import Tbl_Location, Tbl_time
from Guestapp.models import Tbl_Login, Tbl_Customer
from Ownerapp.models import Tbl_Turf, Tbl_turftime


# Create your models here.


class tbl_booking(models.Model):
    bookingid = models.AutoField(primary_key=True)
    customerid = models.ForeignKey(Tbl_Customer, on_delete=models.CASCADE)
    turfid = models.ForeignKey(Tbl_Turf, on_delete=models.CASCADE)
    time = models.ForeignKey(Tbl_time, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    amount = models.BigIntegerField()
    status = models.CharField(max_length=100)


class tbl_payment(models.Model):
    paymentid = models.AutoField(primary_key=True)
    bookingid = models.ForeignKey(tbl_booking, on_delete=models.CASCADE, default="")
    billno = models.BigIntegerField(null=True)
    totalamount = models.BigIntegerField(null=True)
    status = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)