from django.db import models


# Create your models here.
class Tbl_District(models.Model):
    DistrictId = models.AutoField(primary_key=True)
    DistrictName = models.CharField(max_length=50)


class Tbl_Location(models.Model):

    LocationId = models.AutoField(primary_key=True)
    LocationName = models.CharField(max_length=50)
    DistrictId = models.ForeignKey(Tbl_District, on_delete=models.CASCADE)


class Tbl_Category(models.Model):
    CategoryId = models.AutoField(primary_key=True)
    CategoryName = models.CharField(max_length=50)
    CategoryImage = models.ImageField()


class Tbl_time(models.Model):
    TimeId = models.AutoField(primary_key=True)
    Time = models.CharField(max_length=50)


class Tbl_size(models.Model):
    SizeId = models.AutoField(primary_key=True)
    Size = models.CharField(max_length=20)
    Amount = models.BigIntegerField()


