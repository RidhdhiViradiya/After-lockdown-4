import os
from datetime import date, datetime

from django.views.decorators.csrf import csrf_exempt
from payingGuest.PayTm import Checksum

from dateutil.relativedelta import relativedelta
from django.contrib import auth
import calendar
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, BadHeaderError
from django.db.backends import mysql
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessForm, FoodTypesForm
from django.contrib.auth.decorators import login_required
import json
from .models import Mess, Tiffin_types, Food_types, Mess_bookings, MessVendorPayment
from accounts.models import City, Area, User, Packages

MERCHANT_KEY = 'uKc4SdgtR#R8Ri#Y'
# Create your views here.


def add_month(orig_date, months):
    new_year = orig_date.year
    new_month = orig_date.month + months
    while new_month > 12:
        if new_month > 12:
            new_year += 1
            new_month -= 12
    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
    new_day = min(orig_date.day, last_day_of_month)
    
    return orig_date.replace(year=new_year, month=new_month, day=new_day)


def filterdata(request):
    city = request.POST.get('city', '')
    area = request.POST.get('area', '')
    category = request.POST.get('category', '')
    tiffin = request.POST.get('tiffins', '')
    price = int(request.POST.get('price', 0))
    
    first = 0
    num = []
    mycursor = connection.cursor()
    sql = "SELECT mess_id, mess_name, address,image_path FROM mess"
    if city:
        if first == 0:
            sql += " where city=%s"
            first = 1
        else:
            sql += " and where city=%s"
        num.append(city)
    if area:
        if first == 0:
            sql += " where area=%s"
            first = 1
        else:
            sql += " and area=%s"
        num.append(area)
    if category:
        if first == 0:
            sql += " where "
            first = 1
        else:
            sql += " and "
        sql += " mess_id in (select mess_id from food_types where category=%s) "
        num.append(category)
    if price > 10:
        if first == 0:
            sql += " where "
            first = 1
        else:
            sql += " and "
        sql += " mess_id in (select mess_id from food_types where price between 0 and %s) "
        num.append(price)
    if tiffin:
        if first == 0:
            sql += " where "
            first = 1
        else:
            sql += " and "
        sql += " mess_id in (select mess_id from food_types where tiffin_id=%s) "
        num.append(tiffin)
    print(num)
    if first == 0:
        sql += " where is_active=1"
    else:
        sql += " and is_active=1"
    mycursor.execute(sql, num)
    myresult = mycursor.fetchall()
    for result in myresult:
        print(result)

    json_data = json.dumps(myresult)
    return HttpResponse(json_data)


def area_handle(request):
    areas = int(request.POST['id'])
    areas_list = Area.objects.filter(city_id=areas)
    myList = []
    for area in areas_list:
        tup = (area.area_id, area.area_name)
        myList.append(tup)

    json_data = json.dumps(myList)
    return HttpResponse(json_data)


def index(request):
    cities = City.objects.all()
    mess = Mess.objects.filter(is_active=True)
    form = PasswordChangeForm(user=request.user)
    tiffins = Tiffin_types.objects.all()
    datas = {'allmess': mess, 'count': mess.count(), 'cities': cities, 'tiffins': tiffins, 'form': form}
    return render(request, 'food/index.html', datas)


def details(request, id=None):
    mess = get_object_or_404(Mess, mess_id=id)
    foodTypes = Food_types.objects.filter(mess_id=mess)
    categories = foodTypes.values('category').distinct()
    success = 0
    if request.method == 'POST':
        book = Mess_bookings()
        book.user_id = auth.get_user(request)
        book.mess_id = mess
        food = Food_types.objects.get(food_id=request.POST.get('food_id'))
        book.food_id = food
        book.is_active = True
        book.save()
        success = 1
    datas = {'mess': mess, 'food_types': foodTypes, 'success': success,'categories': categories, 'catCount': categories.count()}

    return render(request, 'food/details.html', datas)


# vendor

@login_required(login_url='/accounts/')
def vendor_index(request):
    usr = auth.get_user(request)
    us = User.object.get(user_id=usr.user_id)
    if us.is_foodVendor:
        form = PasswordChangeForm(user=request.user)
        datas = {'form': form}
        return render(request, 'food/vendor/index.html', datas)
    
    else:
        return redirect("/")


@login_required(login_url='/accounts/')
def addmess(request):
    Form = MessForm()
    form = PasswordChangeForm(user=request.user)
    datas = {'Form': Form, 'form': form}
    return render(request, 'food/vendor/addmess.html', datas)


@login_required(login_url='/accounts/')
def addfoodtype(request):
    myMess = Mess.objects.filter(user_id=auth.get_user(request), is_active=True)
    tiffins = Tiffin_types.objects.filter(is_active=True)
    Form = FoodTypesForm(request.POST or None)
    form = PasswordChangeForm(user=request.user)
    datas = {'form': form, 'Form': Form, 'myMess': myMess, 'count': myMess.count(), 'tiffins': tiffins, 'tiffinCount': tiffins.count()}
    return render(request, 'food/vendor/addfoodtype.html', datas)


@login_required(login_url='/accounts/')
def viewmess(request):
    form = PasswordChangeForm(user=request.user)
    if request.GET.get('eid'):
        name = request.POST.get('mname')
        eid = request.GET.get('eid')
        mess = Mess.objects.get(mess_id=eid)
        mess.mess_name = name
        mess.save()
        return redirect('/food/vendor/viewmess')
    elif request.GET.get('did'):
        did = request.GET.get('did')
        mess = Mess.objects.get(mess_id=did)
        mess.delete()
        return redirect('/food/vendor/viewmess')
    else:
        mess = Mess.objects.filter(user_id=auth.get_user(request))
        datas = {'allmess': mess, 'count': mess.count(), 'form': form}
        return render(request, 'food/vendor/viewmess.html', datas)


@login_required(login_url='/accounts/')
def viewfoodtype(request):
    form = PasswordChangeForm(user=request.user)
    if request.GET.get('eid'):
        eid = request.GET.get('eid')
        type = Food_types.objects.get(food_id=eid)
        type.description = request.POST.get('description')
        type.price = request.POST.get('price')
        type.category = request.POST.get('category')
        tiffin_id = request.POST.get('tiffin')
        type.tiffin_id = Tiffin_types.objects.get(type_id=tiffin_id)
        type.save()
        return redirect('/food/vendor/viewfoodtype')
    elif request.GET.get('did'):
        did = request.GET.get('did')
        type = Food_types.objects.get(food_id=did)
        type.delete()
        return redirect('/food/vendor/viewfoodtype')
    else:
        mess = Mess.objects.filter(user_id=auth.get_user(request), is_active=True)
        tiffins = Tiffin_types.objects.filter(is_active=True)
        food_types = Food_types.objects.filter(mess_id__in=mess, is_active=True)
        datas = {'food_types': food_types, 'count': food_types.count(), 'tiffins': tiffins, 'form': form}
        return render(request, 'food/vendor/viewfoodtype.html', datas)


@login_required(login_url='/accounts/')
def manageEmail(request):
    bookings = getBookings(request)
    form = PasswordChangeForm(user=request.user)
    ids = []
    for booking in bookings:
        ids.append(booking.user_id.getuser_id())
    myUsers = User.object.filter(user_id__in=ids)
    myDatas = {'myUsers': myUsers, 'form': form}
    return render(request, 'food/vendor/manageEmail.html', myDatas)


@login_required(login_url="/accounts/")
def sendEmail(request):

    if request.method == 'POST':
        recipients = request.POST.getlist('check')
        sender = auth.get_user(request).email
        password = request.POST.get('password', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        if sender and subject and message and password:
            try:
                send_mail(subject, message, sender, recipients, auth_user=sender, auth_password=password)
            except BadHeaderError:
                return HttpResponse('Invalid Header Encountered')
        else:
            print('Incomplete Details')

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


def getMess(request):
    mess = Mess.objects.filter(user_id=auth.get_user(request))
    return mess


def getBookings(request):
    mess = getMess(request)
    bookings = Mess_bookings.objects.filter(mess_id__in=mess, is_active=True)
    return bookings


@login_required(login_url='/accounts/')
def managestudent(request):
    myBookings = getBookings(request)
    myDatas = {'myBookings': myBookings}
    return render(request, 'food/vendor/managestudent.html', myDatas)


# food
@login_required(login_url="/accounts/")
def delete(request):
    bookingId = request.GET.get('id')
    booking = Mess_bookings.objects.get(booking_id=bookingId)
    booking.is_active = False
    booking.save()
    return redirect('/food/vendor/managestudent')


@login_required(login_url='/accounts/')
def submitMess(request):
    if request.method == 'POST':
        form = MessForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = Mess()
            instance.mess_name = request.POST.get('mess_name', '')
            instance.address = request.POST.get('address', '')
            city_id = request.POST.get('city', '')
            area_id = request.POST.get('area', '')
            instance.city = City.objects.get(city_id=city_id)
            instance.area = Area.objects.get(area_id=area_id)
            myUser = auth.get_user(request)
            usr = User.object.get(user_id=myUser.user_id)
            instance.user_id = usr
            instance.exp_date = datetime.today()
            for file in request.FILES.getlist('image_path'):
                instance.image_path = file
            if instance.exp_date and instance.user_id and instance.mess_name and instance.city and instance.image_path and instance.area and instance.address:
                instance.save()

        else:
            print("Invalid")
            print(form.errors)
        return redirect('/food/vendor/addmess')
    else:
        return render(request, 'food/vendor/addmess.html')


@login_required(login_url='/accounts/')
def submitType(request):
    if request.method == 'POST':
        form = FoodTypesForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = Food_types()
            mess_id = request.POST.get('messid', '')
            tiffin_id = request.POST.get('tiffinid', '')
            instance.mess_id = Mess.objects.get(mess_id=mess_id)
            instance.tiffin_id = Tiffin_types.objects.get(type_id=tiffin_id)
            instance.category = request.POST.get('category', '')
            instance.title = request.POST.get('title', '')
            instance.description = request.POST.get('description', '')
            instance.price = request.POST.get('price', '')
            for file in request.FILES.getlist('image_path'):
                instance.image_path = file
            if instance.mess_id and instance.tiffin_id and instance.category and instance.description and instance.price and instance.image_path:
                instance.save()
        else:
            print(form.errors)
        return redirect('/food/vendor/addfoodtype')
    else:
        return render(request, 'food/vendor/addfoodtype.html')


@login_required(login_url='/accounts/')
def managepayment(request, rid=None):
    packages = Packages.objects.all()
    datas = {'packages': packages, 'rid': rid}
    return render(request, 'food/vendor/managepayment.html', datas)


DURATION = 0
MESS_ID = None
USER_ID = None
ORDER_ID = ''
PID = None


@login_required(login_url='/accounts/')
def payment(request):
    amount = request.POST.get('amount', 0)
    pid = request.POST.get('pid', None)
    id = request.POST.get('rid', '')
    orderid = "F{date}{id}".format(date=datetime.today().strftime('%d%m%y%H'), id=id)
    myUser = auth.get_user(request)
    usr = User.object.get(user_id=myUser.user_id)
    email = usr.get_email()
    global DURATION, MESS_ID, USER_ID, ORDER_ID, PID
    DURATION = request.POST.get('durations', 0)
    MESS_ID = id
    ORDER_ID = orderid
    PID = pid
    USER_ID = myUser.user_id
    
    param_dict = {
        'MID': 'PpHKSz27823539263765',
        'ORDER_ID': orderid,
        'TXN_AMOUNT': '{}'.format(amount),
        'CUST_ID': email,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/food/vendor/payment/handlerequest/',
        
    }
    
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'food/vendor/paytm.html', {'param_dict': param_dict})


@csrf_exempt
def handlerequest(request):
    # handle post request from paytm
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            
            usr = User.object.get(user_id=USER_ID)
            mess = Mess.objects.get(mess_id=MESS_ID)
            package = Packages.objects.get(package_id=PID)
            vendor_pay = MessVendorPayment()
            vendor_pay.mess_id = mess
            vendor_pay.user_id = usr
            vendor_pay.package_id = package
            vendor_pay.order_id = ORDER_ID
            vendor_pay.save()
    
            exp_date = add_month(datetime.today(), int(DURATION))
            mess.exp_date = exp_date
            mess.is_active = True
            mess.save()
            return redirect('view_mess')
        
        else:
            
            print('Payment Unsuccessful because ' + response_dict['RESPMSG'])
    return render(request, 'food/vendor/paymentstatus.html', {'response': response_dict})


