import smtplib
import xlwt

from django.views.generic import View

from email.message import EmailMessage

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from django.views.decorators.cache import cache_control

from Adminapp.models import Tbl_Category, Tbl_size, Tbl_District, Tbl_Location, Tbl_time
from Customerapp.models import tbl_booking
from Guestapp.models import Tbl_Owner, tbl_turfpayment
from Ownerapp.models import Tbl_Turf, Tbl_turftime


# Create your views here.
@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def home(request):
    if "loginid" in request.session:
        loginid = request.session['loginid']
        tb = Tbl_Owner.objects.get(LoginId=loginid)
        id = tb.OwnerId
        # return HttpResponse(id)
        return render(request, "Owner/index.html", {'t': tb})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def turfregistration(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            idm = request.session['loginid']

            cont = Tbl_Owner.objects.get(LoginId=idm)
            id = cont.OwnerId
            email = cont.Email
            # return HttpResponse(email)
            size = request.POST.get('size')
            got = Tbl_size.objects.get(SizeId=size)
            amount = got.Amount
            # return HttpResponse(amount)
            turf = Tbl_Turf()
            turf.TurfName = request.POST.get('name')
            turf.OwnerId = Tbl_Owner.objects.get(OwnerId=id)
            turf.CategoryId = Tbl_Category.objects.get(CategoryId=request.POST.get('category'))
            turf.Size = Tbl_size.objects.get(SizeId=size)
            turf.Image = request.FILES['img']
            turf.Description = request.POST.get('desc')
            turf.LocationId = Tbl_Location.objects.get(LocationId=request.POST.get('location'))
            turf.Amount = amount
            msg = EmailMessage()
            msg.set_content('Turf Registration Successfully Completed')
            msg['Subject'] = "Turf Registration Completed"
            msg['from'] = ('bijalijayalakshmijayan@gmail.com')
            msg['To'] = email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('bijalijayalakshmijayan@gmail.com', 'flva pucy dgan tomw')
                smtp.send_message(msg)

            turf.save()
            return HttpResponse(
                "<script>alert('Your Turf is Successfully Inserted');window.location='/Owner/home/';</script>")
        else:
            tob = Tbl_Category.objects.all()
            tos = Tbl_size.objects.all()
            tod = Tbl_District.objects.all()

            return render(request, "Owner/turfregistration.html", {'tob': tob, 'tos': tos, 'tod': tod})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def turftimereg(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            tob = Tbl_turftime()
            tob.TimeId = Tbl_time.objects.get(TimeId=request.POST.get('time'))
            tob.TurfId = Tbl_Turf.objects.get(TurfId=id)
            tob.save()
            return HttpResponse(
                "<script>alert('Your Time is Successfully Inserted');window.location='/Owner/viewturf/';</script>")
        Turf = Tbl_Turf.objects.get(TurfId=id)
        tbl = Tbl_time.objects.all()
        time = Tbl_turftime.objects.filter(TurfId=id)
        loginid = request.session['loginid']
        tb = Tbl_Owner.objects.get(LoginId=loginid)
        return render(request, "Owner/timereg.html", {'tb': tbl, 'tr': Turf, 'time': time, 't': tb})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def viewturf(request):
    if "loginid" in request.session:
        ob = request.session['loginid']
        # return HttpResponse(ob)
        owner = Tbl_Owner.objects.get(LoginId=ob)
        id = owner.OwnerId
        turf = Tbl_Turf.objects.filter(OwnerId=id)
        loginid = request.session['loginid']
        tb = Tbl_Owner.objects.get(LoginId=loginid)
        return render(request, "Owner/viewturf.html", {'turf': turf, 't': tb})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def viewbookings(request, id):
    if "loginid" in request.session:
        loginid = request.session['loginid']
        tb = Tbl_Owner.objects.get(LoginId=loginid)
        data = tbl_booking.objects.filter(turfid=id, status__in=["paid", "confirmed", "canceled"])
        return render(request, "Owner/viewbookings.html", {"data": data, 't': tb})
    else:
        return HttpResponse("<script>alert('Pls Login');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidation=True, no_store=True)
def logout(request):
    if "loginid" in request.session:
        del request.session['loginid']
        del request.session['uname']
        return HttpResponse("<script>alert('Bye');window.location='/';</script>")


def bookingpiechart(request):
    if "loginid" in request.session:
        login_id = request.session["loginid"]
        loginid = request.session['loginid']
        tb = Tbl_Owner.objects.get(LoginId=loginid)
        t = Tbl_Owner.objects.get(LoginId=login_id)
        id = t.OwnerId

        labels = []
        data = []
        queryset = tbl_booking.objects.filter(turfid__OwnerId=id).values('bookingid').annotate(
            total_owner=Count('turfid'))
        for s in queryset:
            labels.append(s['bookingid'])
            data.append(s['total_owner'])

        return render(request, 'Owner/bookingpiechart.html', {
            'labels': labels,
            'data': data, 't': tb
        })
    else:
        return HttpResponse("<script>alert('You Must Login First');window.location='/login/';</script>")


def BookingExcel(request):
    if "loginid" in request.session:
        login_id = request.session["loginid"]
        # return HttpResponse(login_id)
        t = Tbl_Owner.objects.get(LoginId=login_id)
        id = t.OwnerId
        booking = tbl_booking.objects.filter(turfid__OwnerId=id)
        loginid = request.session['loginid']
        tb = Tbl_Owner.objects.get(LoginId=loginid)
        return render(request, "Owner/BookingExcel.html", {'booking': booking,'t': tb})
    else:
        return HttpResponse("<script>alert('You Must Login First');window.location='/login/';</script>")


class ExportExcel(View):
    def get(self, request):
        login_id = request.session["loginid"]
        # return HttpResponse(login_id)
        t = Tbl_Owner.objects.get(LoginId=login_id)
        id = t.OwnerId
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Turfbooking.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Customer Name', 'Amount', 'Turf', 'Time', 'Status']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)
        queryset = tbl_booking.objects.filter(turfid__OwnerId=id).values_list('customerid__CustomerName', 'amount',
                                                                              'turfid__TurfName', 'time__Time',
                                                                              'status')
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response


def turfpayment(request):
    if request.method == 'POST':
        loginid = request.session['loginid']
        tb = Tbl_Owner.objects.get(LoginId=loginid)
        id = tb.OwnerId
        cob = tbl_turfpayment()
        cob.ownerid = Tbl_Owner.objects.get(OwnerId=id)
        cob.amount = request.POST.get('amount')
        cob.status = 'paid'
        cob.save()
        tb.status = 'paid'
        tb.save()
        return HttpResponse("<script>alert('Payment Successfull');window.location='/Owner/home/';</script>")
    return render(request, "Owner/turfpayment.html")
