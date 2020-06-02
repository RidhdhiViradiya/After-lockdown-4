from accounts.models import PublicQueries, User
from django.contrib import auth, messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.apps import apps


def index(request):
    for app in apps.get_app_configs():
        print(app.verbose_name, ":")
        for model in app.get_models():
            print("\t", model)
    
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        query = PublicQueries()
        query.sender = request.POST.get('name', '')
        query.email = request.POST.get('email', '')
        query.subject = request.POST.get('subject', '')
        query.message = request.POST.get('message', '')
        if query.sender and query.email and query.subject and query.message:
            query.save()
        dict = {'message': 'Your Query Sent successfully!!', 'form': form}
        return render(request, 'index.html', dict)
    else:
        dict = {'form': form}
        return render(request, 'index.html', dict)


@login_required
def update_user(request):
    usr = auth.get_user(request)
    us = User.object.get(user_id=usr.user_id)
    if request.method == 'POST':
        us = User.object.get(user_id=usr.user_id)
        us.first_name = request.POST.get('firstname', '')
        us.email = request.POST.get('email', '')
        us.phone = request.POST.get('phone', '')
        us.gender = request.POST.get('gender', '')
        us.address = request.POST.get('address', '')
        us.is_student = request.POST.get('is_student', 0)
        us.is_pgVendor = request.POST.get('is_pgVendor', 0)
        us.is_foodVendor = request.POST.get('is_foodVendor', 0)
        us.save()
        messages.success(request, 'Changes Saved Successfully!!')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, 'Changes Unsuccessful!!')
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

