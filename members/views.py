from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterUserForm

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
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
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
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
    return render(request, 'members/register.html', {'form':form,})

def delete_user(request):
    if request.method == 'POST':
        request.user.delete() # Delete the user account
        logout(request)  # Log out the user after deleting the account
        messages.success(request, ("You Have Been Logged Out"))
        return redirect('login_user') # Redirect to the login page
    else:
        return render(request, 'members/delete.html')


def profile_user(request):        
    return render(request, 'members/profile.html', {})


def privacy_policy(request):        
    return render(request, 'members/privacy_policy.html', {})