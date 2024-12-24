from http.client import responses

from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee,User
#
from hashlib import md5
def hasher(data):
    # hash data to be stored in cookies
    print(md5(data.encode()).hexdigest())
    return md5(data.encode()).hexdigest()
def index(request):
    if request.method == "POST":
        employment_number = request.POST.get("employmentNumber")
        id_number = request.POST.get("idNumber")
        emp = Employee.objects.filter(emp_num=employment_number , employee_id=id_number).first()
        print(emp)
        if emp:
            if request.session.get("emp_num") is not None:
                del request.session["emp_num"]
                request.session["emp_num"] = hasher(str(str(emp.emp_num) + str(emp.employee_id)) )
            # check if user is valid
            if emp.is_valid:
                return render(request,"dataFin/index.html",context={"msg":"لا يمكن تعديل بياناتك"})
            else:
                # check if user has iban
                if not emp.iban:
                    return render(request,"dataFin/edit_client_data.html",context={"emp":emp})


                return render(request,"dataFin/user_data.html",context={"emp":emp})
        else:
            return render(request,"dataFin/index.html",context={"msg":"البيانات غير صحيحة"})

    return render(request,"dataFin/index.html")

def edit_client(request,id):

    try:
        emp = Employee.objects.get(emp_num=id)
        if request.session.get("emp_num") is None or request.session.get("emp_num") != hasher(str(emp.emp_num) + str(emp.employee_id)):
            return render(request,"dataFin/index.html",context={"msg":"الرجاء التاكد من الرقم الوظيفي"})
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
        if request.session.get("emp_num") == hasher(str(emp_num) + str(emp_id)):
            obj = Employee.objects.get(emp_num=emp_num)
            obj.name = name
            obj.iban = iban
            obj.employee_id = emp_id
            obj.bank = bank
            obj.branch = branch
            obj.is_valid = True
            obj.save()
            return render(request,"dataFin/edit_client_data.html")
        else:
            return render(request,"dataFin/index.html",context={"msg":"الرجاء التاكد من الرقم الوظيفي"})
    return render(request,"dataFin/index.html")
def mark_valid(request,id):
    try:
        if request.session.get("emp_num") == id:
            emp = Employee.objects.get(emp_num=id)
            emp.is_valid = True
            emp.save()
            return render(request, "dataFin/edit_client_data.html", context={"msg": "تم تأكيد بياناتك بنجاح"})
    except Employee.DoesNotExist:
        return render(request, "dataFin/edit_client_data.html", context={"msg": "الرجاء التاكد من الرقم الوظيفي"})


# def migrator(request):
#     emp_obj = Employee.objects.all()
#     print(len(emp_obj))
#     for emp in emp_obj:
#         branch = emp.bank_name.split(" (")
#         if len(branch) == 2:
#             emp.bank_name = branch[0]
#             emp.branch = branch[1].replace(")","")
#             emp.save()
#     return HttpResponse("Done")
#
