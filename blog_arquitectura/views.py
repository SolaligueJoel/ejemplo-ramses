from distutils import errors
from multiprocessing import context
from re import U
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate, login, logout
from blog_arquitectura.forms import User_registration_form
from django.contrib.auth.decorators import login_required

def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                context = {'message': f'Bienvenido {username}'}
                return render(request, 'index.html', context=context)
            else:
                context = {'errors':'No hay ningún registro con esas credenciales'}
                form = AuthenticationForm()
                return render(request, 'auth/login.html', context=context)
        else:
            errors = form.errors
            form = AuthenticationForm()
            context = {'errors':errors,'form':form}
            return render(request, 'auth/login.html', context=context)

    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'auth/login.html', context = context)

def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        form = User_registration_form(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            context = {'message':f'Usuario creado correctamente. Bienvenido {username}'}
            return render(request, 'index.html', context = context)
        else:
            errors = form.errors
            form = User_registration_form()
            context = {'errors':errors, 'form':form}
            return render(request, 'auth/register.html', context = context)

    else:
        form = User_registration_form()
        context = {'form': form}
        return render(request, 'auth/register.html', context=context)

def index(request):
    return render(request,'index.html',context = {})

def about(request):
    return render(request,'about.html',context = {})

@login_required
def contact(request):
    return render(request,'contact.html')