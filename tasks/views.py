from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

# Create your views here.
def home(request):
    return render(request, "home.html")
    
def signup(request):
    msg = ""
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password1"]
        confirm = request.POST["password2"]
        
        if password == confirm:
            try:
                user = User.objects.create_user(username = username, password = password)
                user.save()
                #msg = "user created successfully"
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                msg ="El usuario ya existe!"
        else:
            msg = "Las claves no son iguales"
    
    return render(request, "signup.html", {
        "form": UserCreationForm, "msg": msg
    })

def tasks(request):
    return render(request, "tasks.html")

def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    msg: str = ""
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(
            request, 
            username=username, 
            password= password)
        
        if user is None: msg = "Username or password is incorrect"
        else:
            login(request, user) 
            return redirect("tasks")
        
    return render(request, "signin.html", {
        "form": AuthenticationForm,
        "msg": msg
    })