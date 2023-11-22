from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'Todowoo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'Todowoo/signupuser.html', {'form': UserCreationForm()})
    else:
        # Create a New User
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentTodos')

            except IntegrityError:
                # Tell user that the Username alreay taken
                return render(request, 'Todowoo/signupuser.html', {'form': UserCreationForm(), 'error': 'Sorry, that username is already taken. Choose a different username.'})

        else:
            # Tell user that the passwords don't match
            return render(request, 'Todowoo/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match!'})
        
def Login(request):
    if request.method == 'GET':
        return render(request, 'Todowoo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # Tell user that their account doesn't exist
            return render(request, 'Todowoo/signupuser.html', {'form': UserCreationForm(), 'error': 'User Authentication Failed'})
        else:
            login(request, user)
            return redirect('currentTodos')

@login_required
def Logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required   
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'Todowoo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('currentTodos')
        except ValueError:
            return render(request, 'Todowoo/createtodo.html', {'form': TodoForm(), 'error': "Bad Data put in. Try Again."})


@login_required
def currentTodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'Todowoo/currenttodos.html', {'todos': todos})

@login_required
def completedTodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'Todowoo/completedtodos.html', {'todos': todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'Todowoo/viewtodo.html', {'todo': todo, 'form': form})  
    else:
        form = TodoForm(request.POST, instance=todo)
        try:
            form.save()
            return redirect('currentTodos')
        except ValueError:
            return render(request, 'Todowoo/viewtodos.html', {'todo': todo, 'form': form, 'error': "Bad Data put in. Try Again."})

@login_required        
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currentTodos')

@login_required   
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        # todo.date_completed = timezone.now()
        todo.delete()
        return redirect('currentTodos')