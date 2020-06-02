from django.db.models import Max
from .PayTm import Checksum
from django.http import HttpResponse
from datetime import date
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, get_object_or_404
import json
import calendar
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from accounts.models import City, Area, User, Packages
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .forms import ImageUploadForm
from .models import Room, RoomImage, RoomsBookingDetail, RoomAppointments, Amenities, RoomsVendorPayment
from django.contrib.auth.models import auth
MERCHANT_KEY = 'uKc4SdgtR#R8Ri#Y'
user_id = None
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
    gender = request.POST.get('gender', '')
    price = int(request.POST.get('price', 0))
    amenities = request.POST.get('amenities', '')
    first = 0
    num = []
    mycursor = connection.cursor()
    sql = "SELECT room_id, description, address, image_path FROM rooms"
    if city:
        if first == 0:
            sql += " where area_id in (select area_id from area where city_id = %s) "
            first = 1
        else:
            sql += " and where area_id in (select area_id from area where city_id = %s) "
        num.append(city)
    if area:
        if first == 0:
            sql += " where area_id=%s"
            first = 1
        else:
            sql += " and area_id=%s"
        num.append(area)
    if gender:
        if first == 0:
            sql += " where "
            first = 1
        else:
            sql += " and "
        sql += " gender=%s "
        num.append(gender)
    if amenities:
        if first == 0:
            sql += " where "
            first = 1
        else:
            sql += " and "
        sql += " amenities like '%%{}%%' ".format(amenities)
    if price > 100:
        if first == 0:
            sql += " where "
            first = 1
        else:
            sql += " and "
        sql += " rent_per_bed between 100 and %s "
        num.append(price)
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
    print(areas)
    areas_list = Area.objects.filter(city_id=areas)
    print(areas_list)
    myList = []
    for area in areas_list:
        tup = (area.area_id, area.area_name)
        myList.append(tup)

    print(myList)
    json_data = json.dumps(myList)
    print(json_data)
    return HttpResponse(json_data)


def index(request):
    rooms = Room.objects.filter(is_active=True)
    form = PasswordChangeForm(user=request.user)
    room_images = RoomImage.objects.filter(room_id__in=rooms)
    cities = City.objects.all()
    amenities = Amenities.objects.all()
    datas = {'rooms': rooms, 'count': rooms.count(), 'room_images': room_images, 'cities': cities, 'amenities': amenities, 'form': form}
    return render(request, 'payingGuest/index.html', datas)


def details(request, id=None):
    room = get_object_or_404(Room, room_id=id)
    amenities = room.amenities.split(',')
    if room.special_instruction:
        special = room.special_instruction.split(',')
    else:
        special=''
    room_images = RoomImage.objects.filter(room_id=id)
    datas = {'room': room, 'amenities': amenities, 'room_images': room_images, 'counter': room_images.count(), 'special': special}
    print(room_images.count())
    if request.method == 'POST':
        r = RoomAppointments()
        r.sender = request.POST.get('sender', '')
        r.email = request.POST.get('email', '')
        r.comment = request.POST.get('comment', '')
        r.room_id = Room.objects.get(room_id=id)
        r.user_id = User.object.get(user_id=room.user_id.getuser_id())
        if r.sender and r.email and r.comment:
            r.save()
            datas.update(success='Appointment Booked... You will be contacted by the vendor shortly!!')
        else:
            datas.update(failure='Invalid Information Entered!!')
    return render(request, 'payingGuest/details.html', datas)


def book(request, id=None):
    room = get_object_or_404(Room, room_id=id)
    amenities = room.amenities.split(',')
    room_images = RoomImage.objects.filter(room_id__in=id)
    datas = {'room': room, 'amenities': amenities, 'room_images': room_images, 'counter': room_images.count()}
    
    if request.method == 'POST':
        booking = RoomsBookingDetail()
        booking.is_active = True
        booking.user_id = auth.get_user(request)
        booking.room_id = room
        booking.save()
        rooms = room.vacant_beds
        room.vacant_beds = rooms - 1
        room.save()
    path = "/payingGuest/details/" + id
    return redirect(path)
    

# vendor


@login_required(login_url='/accounts/')
def vendor_index(request):
    usr = auth.get_user(request)
    us = User.object.get(user_id=usr.user_id)
    if us.is_pgVendor:
        form = PasswordChangeForm(user=request.user)
        datas = {'form': form}
        return render(request, 'payingGuest/vendor/index.html', datas)
    else:
        return redirect("/")

# paying Guest


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            print("success")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            print("Unsuccess")
            datas = {'messagess': "Not Valid"}
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


def getRooms(request):
    myUser = auth.get_user(request)
    usr = User.object.get(user_id=myUser.user_id)
    rooms = Room.objects.filter(user_id=usr.user_id)
    rooms_images = RoomImage.objects.filter(room_id__in=rooms)
    return rooms, rooms_images


@login_required(login_url="/accounts/")
def addrooms(request):
    city = City.objects.all()
    packages = Packages.objects.all()
    amenities = Amenities.objects.all()
    form = PasswordChangeForm(user=request.user)
    today = datetime.today().date().strftime('%Y-%m-%d')
    print(today)
    Form = ImageUploadForm(auto_id=False)
    return render(request, 'payingGuest/vendor/addrooms.html', {'today': today, 'form': form, 'cities': city, 'Form': Form, 'packages': packages, 'amenities': amenities})


@login_required(login_url="/accounts/")
def submitRoom(request):
    if request.method == 'POST':
        room = Room()
        room.gender = request.POST['gender']
        room.description = request.POST['description']
        room.no_of_beds = request.POST['totalBeds']
        room.vacant_beds = request.POST['vacantCount']
        room.rent_per_bed = request.POST['rentPerBed']
        room.deposit = request.POST['deposit']
        room.available_from = request.POST['available']
        room.address = request.POST['address']
        room.special_instruction = request.POST['instructions']
        area = request.POST['area']
        amenities = request.POST.getlist('amenities')
        myAmenities = ""
        leng = len(amenities)
        for i in amenities:
            if leng == 1:
                myAmenities += i
            else:
                myAmenities += i + ','
            leng -= 1
        room.amenities = myAmenities
        room.area_id = Area.objects.get(area_id=area)
        myUser = auth.get_user(request)
        usr = User.object.get(user_id=myUser.user_id)
        todays = date.today() + relativedelta(months=+2)
        room.exp_date = datetime.today()
        room.user_id = usr
        room.save()
        user_id = room.room_id
        return redirect('/payingGuest/vendor/addrooms#step-2')
    else:
        print("None")

    return render(request, 'payingGuest/vendor/addrooms.html')


@login_required(login_url="/accounts/")
def upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            loop = 1
            myUser = auth.get_user(request)
            usr = User.object.get(user_id=myUser.user_id)
            room = Room.objects.filter(user_id=usr.user_id).aggregate(maxId=Max('room_id'))
            newRoom = Room.objects.get(room_id=room['maxId'])
            for file in request.FILES.getlist('image'):
                f = RoomImage()
                f.room_id = newRoom
                f.image_path = file
                f.save()
                if loop == 1:
                    loop += 1
                    Room.objects.filter(room_id=room['maxId']).update(image_path=f.image_path)
            return redirect('managepayment', rid=newRoom)
        else:
            messages.info(request, 'Please Select Valid Images!!')
    return redirect('managepayment')


@login_required(login_url="/accounts/")
def viewrooms(request):
    rooms, rooms_images = getRooms(request)
    form = PasswordChangeForm(user=request.user)
    data = {'rooms': rooms, 'form': form, 'room_images': rooms_images, 'rooms_count': rooms.count()}
    return render(request, 'payingGuest/vendor/viewrooms.html', data)


@login_required(login_url="/accounts")
def updaterooms(request):
    if request.method == 'POST':
        roomid = request.GET.get('id')
        room = Room.objects.get(room_id=roomid)
        vacantBeds = request.POST['vacantBeds']
        rentPerBed = request.POST['rentPerBed']
        deposit = request.POST['deposit']
        gender = request.POST['gender']

        room.vacant_beds = vacantBeds
        room.rent_per_bed = rentPerBed
        room.deposit = deposit
        room.gender = gender

        room.save(update_fields=['vacant_beds', 'rent_per_bed', 'deposit', 'gender'])

        print(vacantBeds, rentPerBed, deposit, gender)
        return redirect('/payingGuest/vendor/viewrooms')
    else:
        return redirect('/payingGuest/vendor/viewrooms')


@login_required(login_url="/accounts/")
def managestudent(request):
    myBookings = studentsList(request)
    print(myBookings)
    form = PasswordChangeForm(user=request.user)
    myDatas = {'myBookings': myBookings, 'form': form}
    return render(request, 'payingGuest/vendor/managestudent.html', myDatas)


@login_required(login_url="/accounts/")
def manageappointments(request):
    usr = auth.get_user(request)
    myAppointments = RoomAppointments.objects.filter(user_id=usr)
    print(myAppointments)
    myDatas = {'appointments': myAppointments, 'count': myAppointments.count()}
    return render(request, 'payingGuest/vendor/appointments.html', myDatas)


@login_required(login_url="/accounts/")
def deleteappointment(request):
        appoint = request.GET.get('id')
        appointment = RoomAppointments.objects.filter(appoint_id=appoint).delete()
        return redirect('manageappointments')


@login_required(login_url="/accounts/")
def delete(request):
    bookingId = request.GET.get('id')
    booking = RoomsBookingDetail.objects.get(booking_id=bookingId)
    booking.is_active = False
    booking.save()
    return redirect('/payingGuest/vendor/managestudent')


def studentsList(request):
    rooms = getRooms(request)
    bookings = RoomsBookingDetail.objects.filter(room_id__in=rooms[0], is_active=True)
    return bookings


@login_required(login_url="/accounts/")
def manageEmail(request):
    bookings = studentsList(request)
    form = PasswordChangeForm(user=request.user)
    ids = []
    for booking in bookings:
        ids.append(booking.user_id.getuser_id())
    myUsers = User.object.filter(user_id__in=ids)
    myDatas = {'myUsers': myUsers, 'form': form}
    return render(request, 'payingGuest/vendor/manageEmail.html', myDatas)


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
            print(messages.get_messages(request))
        else:
            print('Incomplete Details')

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/accounts/")
def managepayment(request, rid=None):
    packages = Packages.objects.all()
    datas = {'packages': packages, 'rid': rid}
    return render(request, 'payingGuest/vendor/managepayment.html', datas)


DURATION = 0
ROOM_ID = None
USER_ID = None
ORDER_ID = ''


@login_required(login_url='/accounts/')
def payment(request):
    amount = request.POST.get('amount', 0)
    id = request.POST.get('rid', '')
    orderid = "R{date}{id}".format(date=datetime.today().strftime('%d%m%y%H'), id=id)
    myUser = auth.get_user(request)
    usr = User.object.get(user_id=myUser.user_id)
    email = usr.get_email()
    global DURATION, ROOM_ID, USER_ID, ORDER_ID
    DURATION = request.POST.get('durations', 0)
    ROOM_ID = id
    ORDER_ID = orderid
    USER_ID = myUser.user_id
    
    param_dict = {
            'MID': 'PpHKSz27823539263765',
            'ORDER_ID': orderid,
            'TXN_AMOUNT': '{}'.format(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/payingGuest/vendor/payment/handlerequest/',

    }

    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'payingGuest/vendor/paytm.html', {'param_dict': param_dict})


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
            room = Room.objects.get(room_id=ROOM_ID)
    
            vendor_pay = RoomsVendorPayment()
            vendor_pay.amount = response_dict['TXNAMOUNT']
            vendor_pay.room_id = room
            vendor_pay.user_id = usr
            vendor_pay.order_id = ORDER_ID
            vendor_pay.save()
    
            exp_date = add_month(datetime.today(), int(DURATION))
            room.exp_date = exp_date
            room.is_active = True
            room.save()
            print('Payment Made')
        else:
            print('Payment Unsuccessful because ' + response_dict['RESPMSG'])
    return render(request, 'payingGuest/vendor/paymentstatus.html', {'response': response_dict})

