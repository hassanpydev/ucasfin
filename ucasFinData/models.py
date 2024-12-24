from django.db import models


# Create your models here.
class Employee(models.Model):

    employee_id = models.AutoField(primary_key=True)
    emp_num = models.IntegerField()
    name = models.CharField(max_length=250)
    bank_name = models.CharField(max_length=250)
    branch = models.CharField(max_length=250, null=True, blank=True)
    account_number = models.CharField(max_length=250)
    iban = models.CharField(max_length=250)
    is_valid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    emp_info = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Wallet(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    emp_number = models.IntegerField()
    name = models.CharField(max_length=250)
    id_number = models.CharField(max_length=250)
    birth_date = models.CharField(max_length=15)
    phone = models.CharField(max_length=250)
