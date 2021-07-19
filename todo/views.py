from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Todo
from .forms import TodoForm
# Create your views here.

def home(request):

	return render(request, 'home.html')

def signupuser(request):
	if request.method == 'GET':

		return render(request, 'signupuser.html', {'form': UserCreationForm()})

	else:
		if request.POST['password1'] == request.POST['password2']:

			try:
				user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
				user.save()
				login(request, user)

				return redirect('current') 

			except IntegrityError:
				return render(request, 'signupuser.html', {'form': UserCreationForm(), 'error': 'username already exists '})


		else:
			return render(request, 'signupuser.html', {'form': UserCreationForm(), 'error': 'password not match'})


def logoutuser(request):
	if request.method == 'POST':
		logout(request)

		return redirect('home')


def current(request):

	todos = Todo.objects.filter(user=request.user)
	return render(request, 'current.html', {'todos': todos})

def loginuser(request):
	if request.method == 'GET':
		return render(request, 'loginuser.html', {'form':AuthenticationForm()})

	else:
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request, 'loginuser.html', {'form':AuthenticationForm(), 'error': 'username and password did not match'})
		else:
			login(request, user)
			return redirect('current')

def todolist(request):

	if request.method == 'GET':

		return render(request, 'todolist.html', {'form': TodoForm()})
	else:
		try:
			form = TodoForm(request.POST)
			newtodo = form.save(commit=False)
			newtodo.user = request.user
			newtodo.save()
			return redirect('current')
		except:
			return render(request, 'todolist.html', {'form': TodoForm(), 'error': 'bad datta'})
	

