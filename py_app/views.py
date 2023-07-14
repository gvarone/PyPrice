from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import forms
from py_app.forms import UserForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import requests
import json

historial = []

def base(request):
    response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
    data = json.loads(response.text)
    dolarOficial = float(data[0]['casa']['venta'].replace(",","."))
    dolarBlue = float(data[1]['casa']['venta'].replace(",","."))
    dolarCCL = float(data[3]['casa']['venta'].replace(",","."))
    dolarBolsa = float(data[4]['casa']['venta'].replace(",","."))
    form = forms.FormName()
    context = {}
    context["form"] = form
    context["oficial"] = dolarOficial
    context["blue"] = dolarBlue
    context["ccl"] = dolarCCL
    context["bolsa"] = dolarBolsa
    if request.method == 'POST' and 'submit' in request.POST:
        form = forms.FormName(request.POST)
        if form.is_valid():

            precioOficial = round((form.cleaned_data['precioArs'] / dolarOficial),2)
            precioBlue = round((form.cleaned_data['precioArs'] / dolarBlue),2)
            precioCCL = round((form.cleaned_data['precioArs'] / dolarCCL),2)
            precioBolsa = round((form.cleaned_data['precioArs'] / dolarBolsa),2)

            new_entry = {
                "ref":form.cleaned_data['ref'],
                "pars":form.cleaned_data['precioArs'],
                "poficial": precioOficial,
                "pblue": precioBlue,
                "pccl": precioCCL,
                "pbolsa": precioBolsa,
            }

            historial = request.session.get('historial', [])
            historial.insert(0, new_entry)
            if len(historial) > 5:
                historial = historial[:5]
            request.session['historial'] = historial
            messages.success(request, 'Referencia Guardada Correctamente')
            return HttpResponseRedirect(reverse('py_app:base'))

    if request.method == 'POST' and 'clear' in request.POST:
        if 'historial' in request.session:
            del request.session['historial']
            messages.success(request, 'Historial Eliminado')

    historial = request.session.get('historial',[])
    context["historial"] = historial

    return render(request, 'py_app/base.html',context)


def help(request):
    helpdict = {'help_insert': 'Help Page'}
    return render(request, 'py_app/help.html', context=helpdict)

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,'py_app/registration.html',{'user_form':user_form,'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('py_app:base'))
            else:
                return HttpResponseRedirect("Cuenta no activa")
        else:
            print("Fallo de Login")
            return HttpResponse("Login Invalido")
    else:
        return render(request,'py_app/login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('py_app:base'))