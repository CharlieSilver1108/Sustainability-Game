import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterUserForm, PasswordChangingForm, UpdateUserForm, ProfilePictureForm, addPronounsForm, bioForm
from .models import Profile


# Create your views here.

def login_user(request):
    if request.method == "POST":    # if form has been submitted
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')
            else:
                return redirect('index')
        else:
            messages.success(request, ("Username or Password Incorrect, Please Try Again"))
            return redirect('login_user')
    else:
        return render(request, 'members/login.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out"))
    return redirect('login_user')


def register_user(request):
    if request.method == "POST":    # if form has been submitted
        form = RegisterUserForm(request.POST)   # this form template is in forms.py
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered")
            return redirect('profile_user')
    else:
        form = RegisterUserForm()
    return render(request, 'members/register.html', {'form':form})

def delete_user(request):
    if request.method == 'POST':    # if form has been submit
        request.user.profile.delete()   #delete user profile
        request.user.delete()       # delete user account
        logout(request) 
        messages.success(request, ("You Have Been Logged Out"))
        return redirect('login_user')
    else:
        return render(request, 'members/delete.html')

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm       # this form template is in forms.py
    success_url = reverse_lazy('index')     # if the form is successful, redirect to 'index'


def update_user(request):
    if request.user.is_authenticated:       # check user is logged in
        current_user = User.objects.get(id=request.user.id)
        form1 = UpdateUserForm(request.POST or None, instance=current_user)  # this form template is in forms.py
        form2 = addPronounsForm(request.POST or None, instance=current_user.profile)
        bio_form = bioForm(request.POST or None, instance=current_user.profile)
        if form1.is_valid() and form2.is_valid() and bio_form.is_valid():
            form1.save()
            form2.save()
            bio_form.save()
            login(request, current_user)
            messages.success(request, "Profile Successfully Updated")
            return redirect('profile_user')
        return render(request, 'members/update_user.html', {'form1':form1, 'form2':form2, 'bio_form': bio_form})
    else:
        messages.success(request, "You must be logged in to access this page!")
        return redirect('index')


def profile_user(request):        
    return render(request, 'members/profile.html', {'user': request.user})


def privacy_policy(request):        
    return render(request, 'members/privacy_policy.html', {})

def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_user')  # Redirect to profile view
    else:
        form = ProfilePictureForm(instance=request.user.profile)
    return render(request, 'members/upload_profile_picture.html', {'form': form})