import smtplib
from email.message import EmailMessage

from django.db.models import Max
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from Adminapp.models import Tbl_District, Tbl_Category, Tbl_Location, Tbl_time
from django.http import HttpResponse, JsonResponse

from Customerapp.models import tbl_booking, tbl_payment
from Guestapp.models import Tbl_Customer
from Ownerapp.models import Tbl_Turf, Tbl_turftime


# Create your views here.
@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def index(request):
    if "loginid" in request.session:
        return render(request, "Customer/index.html")
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def searchturf(request):
    if "loginid" in request.session:
        tob = Tbl_Category.objects.all()
        you = Tbl_District.objects.all()
        him = Tbl_Location.objects.all()
        return render(request, "Customer/searchturf.html", {'tob': tob, 'you': you, 'him': him})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def turfview(request):
    if "loginid" in request.session:
        op = request.POST.get('category')
        yo = request.POST.get('location')
        tp = Tbl_Turf.objects.filter(CategoryId=op, LocationId=yo)
        return render(request, "Customer/turfview.html", {'tu': tp})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


def selectloc(request):
    did = int(request.POST.get("did"))
    # return HttpResponse(did)
    location = Tbl_Location.objects.filter(DistrictId=did).values()
    return JsonResponse(list(location), safe=False)


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def viewmore(request, id):
    if "loginid" in request.session:
        turf = Tbl_Turf.objects.filter(TurfId=id)
        time = Tbl_turftime.objects.filter(TurfId=id)
        return render(request, "Customer/viewmore.html", {'turf': turf, 'time': time})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def booking(request, id):
    if "loginid" in request.session:
        if request.method == "POST":
            cust = request.session['loginid']
            cus = Tbl_Customer.objects.get(LoginId=cust)
            c = cus.CustomerId
            time = request.POST.get("time")
            # return HttpResponse(time)
            tob = tbl_booking()
            tob.customerid = Tbl_Customer.objects.get(CustomerId=c)
            tob.turfid = Tbl_Turf.objects.get(TurfId=request.POST.get("name"))
            tob.time = Tbl_time.objects.get(TimeId=time)
            tob.date = request.POST.get("date")
            tob.amount = request.POST.get("amount")
            tob.status = "confirmed"
            tob.save()
            idm = tob.bookingid
            idm_str = str(idm)
            return HttpResponse(
                "<script>alert('Do Payment to confirm your booking');window.location='/Customer/payment/" + idm_str + "';</script>")
        iuf = Tbl_Turf.objects.get(TurfId=id)
        time = Tbl_turftime.objects.filter(TurfId=id)
        return render(request, "Customer/booking.html", {'turf': iuf, 'time': time})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def selecttime(request):
    did = request.POST.get("did")
    td = int(request.POST.get("tid"))
    booked_time_ids = tbl_booking.objects.filter(date=did, turfid=td, status='paid').values_list('time_id',
                                                                                                 flat=True)
    # Filter Tbl_turftime to get available time slots excluding the booked ones
    available_time_slots = Tbl_turftime.objects.filter(TurfId=td).exclude(TimeId__in=booked_time_ids)
    # Convert the queryset to a list of dictionaries
    time = list(available_time_slots.values('TimeId__TimeId', 'TimeId__Time'))
    return JsonResponse(time, safe=False)


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def payment(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            you = tbl_payment()
            you.bookingid = tbl_booking.objects.get(bookingid=id)
            you.totalamount = request.POST.get('amount')
            you.status = 'paid'
            max_bill = tbl_payment.objects.aggregate(max_value=Max('billno'))['max_value']
            if max_bill is not None:
                new_billno = max_bill + 155
            else:
                new_billno = 155
            you.billno = new_billno
            you.save()
            ids = request.session["loginid"]
            customer = Tbl_Customer.objects.get(LoginId=ids)
            customerid = customer.CustomerId
            email = customer.Email
            dob = tbl_booking.objects.get(bookingid=id, customerid=customerid, status="confirmed")
            dob.status = "paid"
            msg = EmailMessage()
            msg.set_content('Your Payment Is completed and Your Booking is conformed')
            msg['Subject'] = "Booking Confirmation"
            msg['from'] = ('bijalijayalakshmijayan@gmail.com')
            msg['To'] = email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('bijalijayalakshmijayan@gmail.com', 'flva pucy dgan tomw')
                smtp.send_message(msg)
            dob.save()
            return HttpResponse("<script>alert('Payment Successful');window.location ='/Customer/index';</script>")
        lid = request.session["loginid"]
        customer = Tbl_Customer.objects.get(LoginId=lid)
        data = tbl_booking.objects.get(bookingid=id)
        return render(request, "Customer/payment.html", {'data': data})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def logout(request):
    if "loginid" in request.session:
        del request.session['loginid']
        del request.session['uname']
        return HttpResponse("<script>alert('Bye');window.location='/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def mybookings(request):
    if "loginid" in request.session:
        idm = request.session['loginid']
        cust = Tbl_Customer.objects.get(LoginId=idm)
        id = cust.CustomerId
        tob = tbl_booking.objects.filter(customerid=id, status='paid')
        return render(request, "Customer/mybookings.html", {'data': tob})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")
