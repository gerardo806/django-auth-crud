from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


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
                user = User.objects.create_user(username=username, password=password)
                user.save()
                # msg = "user created successfully"
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                msg = "El usuario ya existe!"
        else:
            msg = "Las claves no son iguales"

    return render(request, "signup.html", {"form": UserCreationForm, "msg": msg})


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    pending = True
    return render(request, "tasks.html", {"tasks": tasks, "pending": pending})


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by("-datecompleted")
    return render(request, "tasks.html", {"tasks": tasks})


@login_required
def task_detail(request, task_id):
    try:
        # pk: primary key
        # obtener un registro o enviar un 404 -> get_object_or_404
        task = get_object_or_404(Task, pk=task_id, user=request.user)

        if request.method == "GET":
            form = TaskForm(instance=task)
            return render(request, "task_detail.html", {"task": task, "form": form})

        if request.method == "POST":
            form = TaskForm(request.POST, instance=task)
            form.save()

        return redirect("tasks")

    except ValueError:
        err = "Error updating task..."
        return render(
            request, "task_detail.html", {"task": task, "form": form, "error": err}
        )


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")


@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    msg: str = ""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is None:
            msg = "Username or password is incorrect"
        else:
            login(request, user)
            return redirect("tasks")

    return render(request, "signin.html", {"form": AuthenticationForm, "msg": msg})


@login_required
def create_task(request):
    msg = ""
    if request.method == "POST":
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            msg = "Ingrese datos validos"

    return render(request, "create_task.html", {"form": TaskForm, "msg": msg})
