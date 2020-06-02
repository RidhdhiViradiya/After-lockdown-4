from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import City, Area, User
from .forms import CustomUserCreationForm,CustomUserChangeForm, AddUserForm
from django.contrib.auth.models import auth
from django.contrib.auth.password_validation import get_password_validators
import json
# Create your views here.


def index(request):
    creation = CustomUserCreationForm()
    change = CustomUserChangeForm()
    addForm = AddUserForm()
    cities = City.objects.all()
    datas = {'cities': cities, 'add': addForm,'creation': creation, 'change': change}
    return render(request, 'accounts/index.html', datas)


def register(request):
    cities = City.objects.all()
    if request.method == 'POST':
        form = AddUserForm(request.POST or None)
        if form.is_valid():
            print(form.errors)
            myuser = form.save()
            print("Valid")
            messages.success(request, "Registered Successfully !!")
            return redirect('login')
        else:
            print("Invalid")
            for err in form.errors:
                print(err)
            return render(request, 'accounts/index.html', {'add': form, 'cities': cities})
        # print('Ntre Mthod')
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        # usertype = request.POST['usertype']
        # gender = request.POST['gender']
        # email = request.POST['email']
        # password = request.POST['password']
        # phone = request.POST['phone']
        # address = request.POST['address']
        # city = int(request.POST['city'])
        # area = int(request.POST['area'])
        # is_student = 1
        # is_foodVendor = 0
        # is_pgVendor = 0
        # if usertype == 1:
        #     is_student = 1
        #     is_foodVendor = 0
        #     is_pgVendor = 0
        # elif usertype == 2:
        #     is_foodVendor = 1
        #     is_student = 0
        #     is_pgVendor = 0
        # elif usertype == 3:
        #     is_pgVendor = 1
        #     is_student = 0
        #     is_foodVendor = 0
        # myDict = {'message': "Email Already Exists!!", 'cities': cities, 'first_name': first_name, 'last_name': last_name, 'usertype': usertype, 'gender': gender, 'phone': phone, 'address': address, 'city': city, 'area': area}
        # if User.object.filter(email=email).exists():
        #     print("Exists")
        #     return render(request, 'accounts/index.html', myDict)
        # else:
            # areas = Area.objects.get(area_id=area)
            # user = User.object.create_user(first_name, last_name, email, password, gender, address, phone, is_pgVendor, is_foodVendor, is_student, areas)
            # user.save()
            # print("User Created")
            
        return render(request,'accounts/index.html')

    else:
        return render(request,'accounts/index.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            next = request.POST.get('next','/')
            return redirect(next)
        else:
            messages.info(request, 'Invalid Credentials!!')
            return redirect('/accounts/')
    else:
        addForm = AddUserForm()
        return render(request, 'accounts/index.html', {'add': addForm})


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


def area_handle(request):
    id = int(request.POST['id'])
    areas_list = Area.objects.filter(city_id=id)
    myList = []
    for area in areas_list:
        tup = (area.area_id, area.area_name)
        myList.append(tup)

    json_data = json.dumps(myList)
    return HttpResponse(json_data)


