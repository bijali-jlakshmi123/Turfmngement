from datetime import date
from django.db import models
from Adminapp.models import Tbl_Location


# Create your models here.
class Tbl_Login(models.Model):
    LoginId = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Role = models.CharField(max_length=50)
    Status = models.CharField(max_length=50)


class Tbl_Owner(models.Model):
    OwnerId = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    ContactNo = models.BigIntegerField()
    Address = models.CharField(max_length=50)
    LocationId = models.ForeignKey(Tbl_Location, on_delete=models.CASCADE)
    OwnerPhoto = models.ImageField()
    Dob = models.DateField()
    Gender = models.CharField(max_length=50)
    RegDate = models.DateField(default=date.today)
    LoginId = models.ForeignKey(Tbl_Login, on_delete=models.CASCADE)
    status = models.CharField(max_length=60, null=True)


class Tbl_Customer(models.Model):
    CustomerId = models.AutoField(primary_key=True)
    CustomerName = models.CharField(max_length=50)
    Phone = models.BigIntegerField()
    Email = models.CharField(max_length=50)
    LocationId = models.ForeignKey(Tbl_Location, on_delete=models.CASCADE)
    RegDate = models.DateField(auto_now=True)
    LoginId = models.ForeignKey(Tbl_Login, on_delete=models.CASCADE)


class tbl_turfpayment(models.Model):
    paymentid = models.AutoField(primary_key=True)
    ownerid = models.ForeignKey(Tbl_Owner, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    status = models.CharField(max_length=50)
