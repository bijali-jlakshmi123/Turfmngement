import smtplib
from email.message import EmailMessage

import xlwt
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

from Adminapp.models import Tbl_District, Tbl_size
from Adminapp.models import Tbl_Location, Tbl_Category, Tbl_time
from Guestapp.models import Tbl_Owner, Tbl_Login, tbl_turfpayment


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def index(request):
    if "loginid" in request.session:
        return render(request, "Admin/index.html")
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def districtreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            Districtname = request.POST.get('District')

            district = Tbl_District()

            if Tbl_District.objects.filter(DistrictName=Districtname).exists():
                # context={"errror":"Invalid district name"}
                # return render(request,"Admin/districtreg.html",context)
                return HttpResponse(
                    "<script>alert('District Name Already Exists');window.location='/Admin/districtreg/';</script>")
            else:
                district.DistrictName = Districtname
                district.save()  # insert into tablename(Districtname) values(idukki)
                return HttpResponse(
                    "<script>alert('District Inserted');window.location='/Admin/districtreg/';</script>")
        else:
            result = Tbl_District.objects.all()
            return render(request, "Admin/district.html", {'data': result})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


# End of District


def deletedistrict(request, id):
    # return HttpResponse(id)
    district = Tbl_District.objects.get(DistrictId=id)
    district.delete()
    return HttpResponse("<script>alert('District Deleted');window.location='/Admin/districtreg/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def editdistrict(request, id):
    if "loginid" in request.session:
        if request.method == "POST":
            # return HttpResponse("Hai")
            Districtname = request.POST.get('District')

            district = Tbl_District.objects.get(DistrictId=id)
            district.DistrictName = Districtname
            district.save()
            return districtreg(request)
        else:
            district = Tbl_District.objects.get(DistrictId=id)
            return render(request, 'Admin/editdistrict.html', {'district': district})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def locationreg(request):
    if "loginid" in request.session:
        if request.method == "POST":
            # Districtid = request.POST.get('DistrictId')
            Locationname = request.POST.get('location')
            loc = Tbl_Location()
            if Tbl_Location.objects.filter(DistrictId=request.POST.get('DistrictId'),
                                           LocationName=Locationname).exists():
                # context={"errror":"Invalid district name"}
                # return render(request,"Admin/districtreg.html",context)

                return HttpResponse(
                    "<script>alert('District Name Already Exists');window.location='/Admin/locationreg/';</script>")
            else:

                loc.DistrictId = Tbl_District.objects.get(DistrictId=request.POST.get('DistrictId'))

                loc.LocationName = Locationname
                loc.save()  # insert into tablename
                return HttpResponse(
                    "<script>alert('Location Inserted');window.location='/Admin/locationreg/';</script>")
        else:
            result = Tbl_District.objects.all()
            loc = Tbl_Location.objects.all()
            return render(request, "Admin/location.html", {'data': result, 'l': loc})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def editlocation(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            Locationname = request.POST.get('location')

            locobj = Tbl_Location.objects.get(LocationId=id)
            locobj.LocationName = Locationname
            locobj.save()

            return locationreg(request)
        else:
            result = Tbl_District.objects.all()
            locobj = Tbl_Location.objects.get(LocationId=id)
            return render(request, 'Admin/editlocation.html', {'data': result, 'locobj': locobj})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


def deletelocation(request, id):
    locobj = Tbl_Location.objects.get(LocationId=id)
    locobj.delete()
    return HttpResponse("<script>alert('Location Deleted');window.location='/Admin/locationreg/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def categoryreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            catname = request.POST.get("category")

            catobj = Tbl_Category()
            catobj.CategoryName = catname

            if len(request.FILES) != 0:
                catimg = request.FILES['categoryimage']
            else:
                catimg = 'Images/default.jpg'
            catobj.CategoryImage = catimg
            catobj.save()
            return HttpResponse(
                "<script>alert('Category Registered Sucessfully');window.location='/Admin/categoryreg/';</script>")
        else:
            catobj = Tbl_Category.objects.all()

            return render(request, "Admin/category.html", {'data': catobj})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def editcategory(request, id):
    if "loginid" in request.session:
        if request.method == "POST":
            # return HttpResponse("Hai")
            catname = request.POST.get("category")

            catobj = Tbl_Category.objects.get(CategoryId=id)
            catobj.CategoryName = catname
            catobj.save()
            return redirect('/Admin/categoryreg/')
        else:
            catobj = Tbl_Category.objects.get(CategoryId=id)
            return render(request, 'Admin/editcategory.html', {'cate': catobj})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


def deletecategory(request, id):
    catobj = Tbl_Category.objects.get(CategoryId=id)
    catobj.delete()
    return HttpResponse("<script>alert('Category Deleted');window.location='/Admin/categoryreg/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def timereg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            tym = request.POST.get('time')
            Tim = Tbl_time()
            if Tbl_time.objects.filter(Time=tym).exists():
                return HttpResponse(
                    "<script>alert('Time Registered Sucessfully');window.location='Admin/timereg/';</script>")
            else:
                Tim.Time = tym
                Tim.save()
                return HttpResponse("<script>alert('Time Inserted');window.location='/Admin/timereg/';</script>")
        else:
            ress = Tbl_time.objects.all()
            return render(request, "Admin/time.html", {'ds': ress})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def edittime(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            tym = request.POST.get('time')
            Tim = Tbl_time.objects.get(TimeId=id)
            Tim.Time = tym
            Tim.save()
            return HttpResponse("<script>alert('Time Updated');window.location='/Admin/timereg/';</script>")

        else:
            res = Tbl_time.objects.get(TimeId=id)
            return render(request, "Admin/edittime.html", {'d': res})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def sizereg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            size = request.POST.get('size')
            Amount = request.POST.get('amount')
            tob = Tbl_size()
            tob.Size = size
            tob.Amount = Amount
            tob.save()
            return HttpResponse("<script>alert('Size Inserted');window.location='/Admin/sizereg/';</script>")
        else:
            data = Tbl_size.objects.all()
            return render(request, "Admin/size.html", {'data': data})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def editsize(request, id):
    if "loginid" in request.session:
        if request.method == "POST":
            # return HttpResponse("Hai")
            size = request.POST.get("size")
            amount = request.POST.get("amount")
            catobj = Tbl_size.objects.get(SizeId=id)
            catobj.Size = size
            catobj.Amount = amount
            catobj.save()
            return HttpResponse("<script>alert('Size Updated');window.location='/Admin/sizereg/';</script>")
        else:
            data = Tbl_size.objects.get(SizeId=id)
            return render(request, "Admin/editsize.html", {'cate': data})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


def deletesize(request, id):
    catobj = Tbl_size.objects.get(SizeId=id)
    catobj.delete()
    return HttpResponse("<script>alert('Size Deleted');window.location='/Admin/sizereg/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def verification(request):
    if "loginid" in request.session:
        data = Tbl_Owner.objects.filter(LoginId__Status='requested')
        return render(request, 'Admin/verification.html', {'data': data})
    else:
        return HttpResponse("<script>alert('You Must Login First');window.location='/login/';</script>")


def accept(request, id):
    data = Tbl_Login.objects.get(LoginId=id)
    e = Tbl_Owner.objects.get(LoginId=id)
    email = e.Email
    data.Status = "confirmed"
    msg = EmailMessage()
    msg.set_content('Your Account is successfully Verified')
    msg['Subject'] = "verified"
    msg['from'] = ('bijalijayalakshmijayan@gmail.com')
    msg['To'] = email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('bijalijayalakshmijayan@gmail.com', 'flva pucy dgan tomw')
        smtp.send_message(msg)
    data.save()
    return HttpResponse("<script>alert('U accepted the owner');window.location='/Admin/verification/';</script>")


def reject(request, id):
    data = Tbl_Login.objects.get(LoginId=id)
    e = Tbl_Owner.objects.get(LoginId=id)
    email = e.Email
    data.Status = "rejected"
    msg = EmailMessage()
    msg.set_content('Your Account is Rejected by the Admin')
    msg['Subject'] = "Rejected"
    msg['from'] = ('bijalijayalakshmijayan@gmail.com')
    msg['To'] = email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('bijalijayalakshmijayan@gmail.com', 'flva pucy dgan tomw')
        smtp.send_message(msg)
    data.save()
    return HttpResponse("<script>alert('U rejected the owner');window.location='/Admin/verification/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def logout(request):
    if "loginid" in request.session:
        del request.session['loginid']
        del request.session['uname']
        return HttpResponse("<script>alert('Bye');window.location='/';</script>")


def ownerreport(request):
    if "loginid" in request.session:
        labels = ['Accepted', 'Rejected']  # Labels for accepted and rejected registrations
        data = []

        accepted_count = Tbl_Owner.objects.filter(LoginId__Status='confirmed').count()
        rejected_count = Tbl_Owner.objects.filter(LoginId__Status='Rejected').count()

        data.append(accepted_count)
        data.append(rejected_count)

        return render(request, 'Admin/ownerreport.html', {
            'labels': labels,
            'data': data,
        })
    else:
        return HttpResponse("<script>alert('You Must Login First');window.location='/login/';</script>")


def locationreport(request):
    if "loginid" in request.session:
        labels = []
        data = []

        queryset = Tbl_Owner.objects.values('LocationId__LocationName').annotate(total_owner=Count('OwnerId'))
        for s in queryset:
            labels.append(s['LocationId__LocationName'])
            data.append(s['total_owner'])

        return render(request, 'Admin/locationreport.html', {
            'labels': labels,
            'data': data,
        })
    else:
        return HttpResponse("<script>alert('You Must Login First');window.location='/login/';</script>")


def viewturfpayment(request):
    tbl = tbl_turfpayment.objects.all()
    return render(request, "Admin/viewturfpayment.html", {'tbl': tbl})


def paymentexcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Turfbooking.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sheet1')

    # Define the column headings
    row_num = 0
    columns = ['Owner Name', 'Phone Number', 'Amount', 'Status']
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Fetch data from the database
    queryset = tbl_turfpayment.objects.all().values_list('ownerid__FirstName', 'ownerid__ContactNo',
                                                         'amount', 'status')

    # Write data to Excel sheet
    for row in queryset:
        row_num += 1
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, str(cell_value))  # Ensure cell values are strings

    # Save workbook to the HttpResponse
    wb.save(response)
    return response
