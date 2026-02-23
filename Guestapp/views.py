import smtplib
from email.message import EmailMessage

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from Adminapp.models import Tbl_District, Tbl_Location
from Guestapp.models import Tbl_Login, Tbl_Owner, Tbl_Customer


# Create your views here.
def index(request):
    return render(request, "Guest/index.html")
    # page load


def ownerregistration(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('password')
        lobj = Tbl_Login()
        if Tbl_Login.objects.filter(UserName=username, Password=password).exists():
            return HttpResponse(
                "<script>alert('The Username and Password are Taken');window.location='/login/';</script>")
        lobj.UserName = username
        lobj.Password = password
        lobj.Role = 'owner'
        lobj.Status = 'requested'
        email = request.POST.get('email')
        own = Tbl_Owner()
        if len(request.FILES) != 0:
            ophoto = request.FILES['photo']
        else:
            ophoto = 'images/default.jpeg'
        own.FirstName = request.POST.get('fname')
        own.LastName = request.POST.get('lname')
        own.Email = email
        own.ContactNo = request.POST.get('cno')
        own.Address = request.POST.get('address')
        own.Dob = request.POST.get('dob')
        own.Gender = request.POST.get('gender')
        own.OwnerPhoto = ophoto
        own.LocationId = Tbl_Location.objects.get(LocationId=request.POST.get('location'))
        lobj.save()

        own.LoginId = lobj

        msg = EmailMessage()
        msg.set_content('Registration Successfully Completed')
        msg['Subject'] = "Owner Registration Completed"
        msg['from'] = ('bijalijayalakshmijayan@gmail.com')
        msg['To'] = email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('bijalijayalakshmijayan@gmail.com', 'flva pucy dgan tomw')
            smtp.send_message(msg)

        own.save()
        return HttpResponse(
            "<script>alert('Your Data Is Inserted');window.location='/ownerregistration/';</script>")
    else:
        location = Tbl_Location.objects.all()
        district = Tbl_District.objects.all()
        return render(request, "Guest/ownerregistration.html", {'district': district, 'location': location})


def selectlocation(request):
    did = int(request.POST.get("did"))
    # return HttpResponse(did)
    location = Tbl_Location.objects.filter(DistrictId=did).values()
    return JsonResponse(list(location), safe=False)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Tbl_Login.objects.filter(UserName=username, Password=password).exists():
            data = Tbl_Login.objects.get(UserName=username, Password=password)
            request.session['uname'] = data.UserName
            request.session['loginid'] = data.LoginId
            role = data.Role
            status = data.Status
            if role == 'Admin' and status == 'confirmed':
                return redirect('/Admin/index/')
            elif role == 'owner' and status == 'confirmed':
                return redirect('/Owner/home/')
            elif role == 'customer' and status == 'confirm':
                return redirect('/Customer/index/')
            else:
                return HttpResponse("Not approved")
        else:
            context = {"error": "Incorrect username or password"}
            return render(request, "guest/login.html", context)
    else:
        return render(request, "Guest/login.html")


def customerreg(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('password')
        lobj = Tbl_Login()
        if Tbl_Login.objects.filter(UserName=username, Password=password).exists():
            return HttpResponse(
                "<script>alert('Your Name And Password are Taken');window.location='/login/';</script>")
        lobj.UserName = username
        lobj.Password = password
        lobj.Role = 'customer'
        lobj.Status = 'confirm'
        lobj.save()
        email=request.POST.get('email')
        cust = Tbl_Customer()
        cust.CustomerName = request.POST.get('name')
        # return HttpResponse(cust.Name)
        cust.Email = email
        cust.Phone = request.POST.get('cno')
        cust.LocationId = Tbl_Location.objects.get(LocationId=request.POST.get('location'))
        cust.LoginId = lobj
        msg = EmailMessage()
        msg.set_content('Registration Successfully Completed')
        msg['Subject'] = "Customer Registration Completed"
        msg['from'] = ('bijalijayalakshmijayan@gmail.com')
        msg['To'] = email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('bijalijayalakshmijayan@gmail.com', 'flva pucy dgan tomw')
            smtp.send_message(msg)

        cust.save()
        return HttpResponse(
            "<script>alert('Your Data Is Inserted');window.location='/login/';</script>")

    location = Tbl_Location.objects.all()
    district = Tbl_District.objects.all()
    return render(request, "guest/customerregistration.html", {'loc': location, 'dis': district})
