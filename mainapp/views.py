from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, DetailsForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate

# Create your views here.
def index(request):
    form = DetailsForm
    return render(request, "index.html", {'form': form})

def login(request):
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
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = CreateUserForm()
    return render(request, 'auth/signup.html', {'form': form})

def logout(request):
    if request.method == "POST":
        print("logging out")
        auth_logout(request)
    return redirect("/")

def updateDetails(request):
    if request.method == "POST":
        form = DetailsForm
        pass
    form = DetailsForm
    return render(request, "profile/details.html", {"form": form})