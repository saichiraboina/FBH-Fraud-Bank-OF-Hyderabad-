from django.db import models

# Create your models here.
class Account(models.Model):
    Name = models.CharField(max_length = 36)
    DOB = models.DateField()
    Aadhar = models.BigIntegerField()
    Pan = models.CharField(max_length = 10)
    Mobile = models.IntegerField()
    Address = models.CharField(max_length = 50)
    Account_no = models.BigAutoField(primary_key=True)
    Pin = models.IntegerField(default=0)
    Balance = models.DecimalField(max_digits = 7 ,decimal_places = 2,default = 1000.00)
    OTP = models.IntegerField(default = 0)
    email = models.EmailField(default='saichiraboina14@gmail.com')