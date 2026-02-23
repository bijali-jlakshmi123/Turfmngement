from django.db import models

from Adminapp.models import Tbl_Category, Tbl_size, Tbl_Location, Tbl_time
from Guestapp.models import Tbl_Owner


# Create your models here.


class Tbl_Turf(models.Model):
    TurfId = models.AutoField(primary_key=True)
    TurfName = models.CharField(max_length=40)
    OwnerId = models.ForeignKey(Tbl_Owner, on_delete=models.CASCADE)
    RegDate = models.DateField(auto_now=True)
    CategoryId = models.ForeignKey(Tbl_Category, on_delete=models.CASCADE)
    Image = models.ImageField()
    LocationId = models.ForeignKey(Tbl_Location, on_delete=models.CASCADE, null=True)
    Description = models.CharField(max_length=2000)
    Amount = models.BigIntegerField()
    Size = models.ForeignKey(Tbl_size, on_delete=models.CASCADE)


class Tbl_turftime(models.Model):
    tid = models.AutoField(primary_key=True)
    TurfId = models.ForeignKey(Tbl_Turf, on_delete=models.CASCADE)
    TimeId = models.ForeignKey(Tbl_time, on_delete=models.CASCADE)
