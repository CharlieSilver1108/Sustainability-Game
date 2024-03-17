import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterUserForm, PasswordChangingForm, UpdateUserForm, ProfilePictureForm, addPronounsForm, bioForm
from .models import Profile, ProfileBadgeRelation, Badge

# Create your views here.

# ------- Charlie START -------

# login_user checks if the form has been submit, and if not it renders the 'login.html' template
def login_user(request):
    if request.method == "POST":    # if form has been submitted
        username = request.POST['username']     # sets username and password from the form in the 'login.html' template
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)      # django.contrib.auth.authenticate to check user is valid
        if user is not None:
            login(request, user)                                                # django.contrib.auth.login creates the user session
            return redirect('index')
        else:
            messages.success(request, ("Username or Password Incorrect, Please Try Again"))     # outputs a message to the user if they have input invalid credentials
            return redirect('login_user')
    else:
        return render(request, 'members/login.html', {})


# logout_user uses django.contrib.auth.logout to destroy the current user session and then redirects to the login page, displaying a success message
def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out"))
    return redirect('login_user')


# register_user checks if the form has been submit, and if not it renders the 'register.html' template
def register_user(request):
    if request.method == "POST":    # if form has been submit
        form = RegisterUserForm(request.POST)   # this form template is in forms.py
        if form.is_valid():
            form.save()            # saves data into database
            username = form.cleaned_data['username']            # logs the user into the account they have just created
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered")
            return redirect('profile_user')
    else:
        form = RegisterUserForm()
    return render(request, 'members/register.html', {'form':form})


# delete_user ensures the user is signed in, then if the form has been submit, and if not it renders the 'delete.html' template
def delete_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':    # if form has been submit
            request.user.profile.delete()   #delete user profile - before the user account (important since there would be no access to the user profile if account was deleted first)
            request.user.delete()       # delete user account
            logout(request) 
            messages.success(request, ("You Have Been Logged Out"))
            return redirect('login_user')
        else:
            return render(request, 'members/delete.html')
    else:
        messages.success(request, "You must be logged in to access that page!")         # if user is not logged in, redirects to home page and displays message
        return redirect('index')


# PasswordsChangeView displays the PasswordChangeView, and redirects if the form is successful
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm       # this form template is in forms.py
    success_url = reverse_lazy('index')     # if the form is successful, redirect to 'index'


# update_user ensures that the user is logged in, and then displays the form to update their profile if they are
def update_user(request):
    if request.user.is_authenticated:       # check user is logged in
        current_user = User.objects.get(id=request.user.id)
        form1 = UpdateUserForm(request.POST or None, instance=current_user)  # this form template is in forms.py
        form2 = addPronounsForm(request.POST or None, instance=current_user.profile)
        bio_form = bioForm(request.POST or None, instance=current_user.profile)
        if form1.is_valid() and form2.is_valid() and bio_form.is_valid():
            form1.save()
            form2.save()
            bio_form.save()            # saves data into database
            login(request, current_user)
            messages.success(request, "Profile Successfully Updated")
            return redirect('profile_user')
        return render(request, 'members/update_user.html', {'form1':form1, 'form2':form2, 'bio_form': bio_form})
    else:
        messages.success(request, "You must be logged in to access that page!")         # if user is not logged in, redirects to home page and displays message
        return redirect('index')

# profile_viewer receives a paramater from the URL corresponding to an existing User's username
# it allows a user to view their friend's profile, for example
def profile_viewer(request, username=None):
    try:
        userToView = User.objects.get(username=username)             # either returns a User object, or a 404 error saying the user doesn't exist
        user_position = list(Profile.objects.order_by('-points')).index(Profile.objects.get(user=userToView)) + 1
        badges_with_dates = ProfileBadgeRelation.objects.filter(profile=userToView.profile)
        return render(request, 'members/profileViewer.html', {'userToView': userToView, 'user_position':user_position, 'badges_with_dates':badges_with_dates})
    except:
        messages.success(request, "User not found!")         # if no parameter value is given, redirects to home page and displays message
        return redirect('index')

# privacy_policy simply displays the 'privacy_policy.html' template
def privacy_policy(request):        
    return render(request, 'members/privacy_policy.html', {})

# ------- Charlie END -------



# ------- Will START -------
def profile_user(request):#
    current_user_position = list(Profile.objects.order_by('-points')).index(Profile.objects.get(user=request.user)) + 1
    badges_with_dates = ProfileBadgeRelation.objects.filter(profile=request.user.profile)
    return render(request, 'members/profile.html', {'user': request.user, 'user_position':current_user_position, 'badges_with_dates':badges_with_dates})
# ------- Will END -------


# ------- Liam START -------
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()            # saves data into database
            return redirect('profile_user')  # Redirect to profile view
    else:
        form = ProfilePictureForm(instance=request.user.profile)
    return render(request, 'members/upload_profile_picture.html', {'form': form})
# ------- Liam END -------