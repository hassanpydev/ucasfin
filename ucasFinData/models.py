from django.db import models

# Create your models here.
class Employee(models.Model):
    _tablename_ = 'employees'
    employee_id = models.AutoField(primary_key=True)
    emp_num = models.IntegerField()
    name = models.CharField(max_length=250)
    bank_name = models.CharField(max_length=250)
    branch = models.CharField(max_length=250,null=True,blank=True)
    account_number = models.CharField(max_length=250)
    iban = models.CharField(max_length=250)
    is_valid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
