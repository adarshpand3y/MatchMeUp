from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, LoginForm, DetailsForm
from .models import Profile

import os
from dotenv import load_dotenv

load_dotenv()

CLOUD_NAME = os.environ.get("CLOUD_NAME")

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        users = User.objects.filter()
        return render(request, "index_logged_in.html", {"users": users, "cloud_name": CLOUD_NAME})
    return render(request, "index.html")

def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    errorMessage = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid:
            username = form['username'].value()
            password = form['password'].value()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect("/")
                else:
                    errorMessage = "Invalid Credentials"
            else:
                errorMessage = "Invalid Credentials"
    form = LoginForm
    return render(request, "auth/login.html", {'form': form, "error": errorMessage})

def signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/updateDetails')
    else:
        form = CreateUserForm()
    return render(request, 'auth/signup.html', {'form': form})

@login_required(login_url="/login")
def logout(request):
    if request.method == "POST":
        auth_logout(request)
    return redirect("/")

@login_required(login_url="/login")
def updateDetails(request):
    details_instance, details_created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = DetailsForm(request.POST, request.FILES, instance=details_instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            # return render(request, "profile/details.html", {"form": form, "message":"Details updated!"})
            return redirect(f"/profile/{request.user}")
    form = DetailsForm(instance=details_instance)
    return render(request, "profile/details.html", {"form": form})

@login_required(login_url="/login")
def profile(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    return render(request, "profile/profile.html", {"user": user, "profile": profile, "cloud_name": CLOUD_NAME})
