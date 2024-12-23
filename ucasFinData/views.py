from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
# Create your views here.
def index(request):
    if request.method == "POST":
        employment_number = request.POST.get("employmentNumber")
        id_number = request.POST.get("idNumber")
        emp = Employee.objects.filter(emp_num=employment_number , employee_id=id_number).first()
        if emp:
            return render(request,"dataFin/edit_client_data.html",context={"emp":emp})
        else:
            return HttpResponse("User Not Found")

    return render(request,"dataFin/edit_client_data.html")

def edit_client(request,id):
    try:
        emp = Employee.objects.get(emp_num=id)
        if emp.is_valid:
            return render(request,"dataFin/edit_client_data.html",context={"msg":"لم يمكن تعديل بياناتك"})
        return render(request,"dataFin/edit_client_data.html",context={"emp":emp})
    except Employee.DoesNotExist:
        return render(request,"dataFin/edit_client_data.html",context={"msg":"الرجاء التاكد من الرقم الوظيفي"})

def save_client_data(request):
    if request.method == "POST":
        name = request.POST.get("name")
        emp_num = request.POST.get("emp_num")
        iban = request.POST.get("iban")
        emp_id = request.POST.get("id")
        bank = request.POST.get("bank")
        branch = request.POST.get("branch")
        obj = Employee.objects.get(emp_num=emp_num)
        obj.name = name
        obj.iban = iban
        obj.employee_id = emp_id
        obj.bank = bank
        obj.branch = branch
        obj.is_valid = True
        obj.save()
        return render(request,"")
