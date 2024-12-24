from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee, Wallet

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
        emp = Employee.objects.filter(
            emp_num=employment_number, employee_id=id_number
        ).first()
        print(emp)
        if emp:
            if request.session.get("emp_num") is not None:
                del request.session["emp_num"]
                request.session["emp_num"] = hasher(
                    str(str(emp.emp_num) + str(emp.employee_id))
                )
            # check if user is valid
            if emp.is_valid:
                return render(
                    request,
                    "dataFin/index.html",
                    context={"msg": "لا يمكن تعديل بياناتك"},
                )
            else:
                # check if user has iban
                if not emp.iban:
                    return render(
                        request, "dataFin/edit_client_data.html", context={"emp": emp}
                    )

                return render(request, "dataFin/user_data.html", context={"emp": emp})
        else:
            return render(
                request, "dataFin/index.html", context={"msg": "البيانات غير صحيحة"}
            )

    return render(request, "dataFin/index.html")


def edit_client(request, id):

    try:
        emp = Employee.objects.get(emp_num=id)
        if request.session.get("emp_num") is None or request.session.get(
            "emp_num"
        ) != hasher(str(emp.emp_num) + str(emp.employee_id)):
            return render(
                request,
                "dataFin/index.html",
                context={"msg": "الرجاء التاكد من الرقم الوظيفي"},
            )
        if emp.is_valid:
            return render(
                request,
                "dataFin/edit_client_data.html",
                context={"msg": "لم يمكن تعديل بياناتك"},
            )
        return render(request, "dataFin/edit_client_data.html", context={"emp": emp})
    except Employee.DoesNotExist:
        return render(
            request,
            "dataFin/edit_client_data.html",
            context={"msg": "الرجاء التاكد من الرقم الوظيفي"},
        )


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
            return render(request, "dataFin/edit_client_data.html")
        else:
            return render(
                request,
                "dataFin/index.html",
                context={"msg": "الرجاء التاكد من الرقم الوظيفي"},
            )
    return render(request, "dataFin/index.html")


def mark_valid(request, id):
    try:
        if request.session.get("emp_num") == id:
            emp = Employee.objects.get(emp_num=id)
            emp.is_valid = True
            emp.save()
            return render(
                request,
                "dataFin/edit_client_data.html",
                context={"msg": "تم تأكيد بياناتك بنجاح"},
            )
    except Employee.DoesNotExist:
        return render(
            request,
            "dataFin/edit_client_data.html",
            context={"msg": "الرجاء التاكد من الرقم الوظيفي"},
        )


def format_date_from_db(date):
    try:
        return datetime.strptime(date, "%m/%d/%y")
    except BaseException as e:
        print(e)


def format_date_from_web(date):
    parsed_date = datetime.strptime(date, "%Y-%m-%d")

    # Add the time component and format it
    formatted_date = parsed_date.strftime("%Y-%m-%d 00:00:00")
    return formatted_date


def wallet(request):
    # verify post data and match data: emp_num, id_number,birth_date
    if request.method == "POST":
        emp_num = request.POST.get("emp_num")
        id_number = request.POST.get("id_number")
        birth_date = request.POST.get("birth_date")

        wallet_ = Wallet.objects.get(emp_number=emp_num, id_number=id_number)
        if wallet_:
            print("Date from db", format_date_from_db(wallet_.birth_date))
            print("Date from web", format_date_from_web(birth_date))
            if str(format_date_from_db(wallet_.birth_date)) == str(
                format_date_from_web(birth_date)

            ):
                request.session["wallet"] = hasher(str(id_number))
                return render(
                    request, "dataFin/wallet_update.html", context={"wallet_": wallet_}
                )
            return HttpResponse("User not found")
        else:
            return HttpResponse("User not found")

    return render(request, "dataFin/wallet.html")


def wallet_update(request):
    if request.method == "POST":
        # Get form data
        emp_number = request.POST.get("emp_number")
        id_number = request.POST.get("id_number")
        phone = request.POST.get("phone")
        print(emp_number, id_number, phone)
        if request.session.get("wallet") == hasher(str(id_number)):
            # validate data
            wallet_ = Wallet.objects.get(emp_number=emp_number, id_number=id_number)
            wallet_.phone = phone
            wallet_.save()
            return render(request, "dataFin/wallet.html", context={"msg": "تم تحديث البيانات بنجاح"})
        else:
            return render(
                request,
                "dataFin/index.html",
                context={"msg": "الرجاء التاكد من الرقم الوظيفي"},
            )
    return render(request, "dataFin/wallet.html")
