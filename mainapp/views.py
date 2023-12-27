from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import CreateUserForm, LoginForm, DetailsForm, MatchRequestForm, MatchForm
from .models import Profile, Match, MatchRequest

import os
from dotenv import load_dotenv

load_dotenv()

CLOUD_NAME = os.environ.get("CLOUD_NAME")

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        traget_gender = "m" if request.user.profile.gender == "f" else "f"
        users = User.objects.filter(is_active=True, is_staff=False, profile__gender=traget_gender)
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
    isRequestSent = MatchRequest.objects.filter(sent_by=request.user, sent_to=User.objects.get(username=username)).exists()
    isMatched = True if len(Match.objects.filter(Q(user1=request.user, user2=user) | Q(user1=user, user2=request.user))) == 1 else False
    return render(request, "profile/profile.html", {"user": user, "profile": profile, "cloud_name": CLOUD_NAME, "isRequestSent": isRequestSent, "isMatched": isMatched})

@login_required(login_url="/login")
def sendMatchRequest(request):
    if request.method == 'POST':
        # Create a form instance, but we won't use it to validate or display any fields
        sent_from = request.user
        sent_to = User.objects.get(username=request.POST.get('sent_to'))
        if not MatchRequest.objects.filter(sent_by=request.user, sent_to=sent_to).exists():
            # Create a Match instance
            match_request = MatchRequest.objects.create(sent_by=request.user, sent_to=sent_to)
            match_request.save()

            # Checking if a request exists for the same people but other way around.
            # If so, create a match object
            if MatchRequest.objects.filter(sent_by=sent_to, sent_to=request.user).exists():
                user_match = Match(user1=request.user, user2=sent_to)
                user_match.save()
                
    return redirect(f'/profile/{sent_to}')

@login_required(login_url="/login")
def matches(request):
    matches = Match.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    matchData = []
    for m in matches:
        if m.user1 == request.user:
            matchData.append(m.user2)
        else:
            matchData.append(m.user1)
    return render(request, "matches.html", {"matches": matches, "matchData": matchData, "cloud_name": CLOUD_NAME})