from django.contrib import admin
from .models import Employee
# Register your models here.

from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = (
    'employee_id', 'emp_num', 'name', 'bank_name', 'branch', 'account_number', 'iban', 'is_valid')


    # Fields to filter the list by
    list_filter = ('bank_name', 'branch', 'is_valid', 'created_at')

    # Fields to search by in the admin
    search_fields = ('name', 'emp_num', 'bank_name', 'account_number', 'iban')

    # Fields to group in the admin detail view
    fieldsets = (
        ('بيانات الموظف', {
            'fields': ('emp_num', 'name', 'bank_name', 'branch', 'account_number', 'iban')
        }),
        ('حالة البيانات', {
            'fields': ('صحيحة',)
        }),
        ('تاريخ الحركات على البيانات', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    # Read-only fields
    readonly_fields = ('created_at', 'updated_at')

