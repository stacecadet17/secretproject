# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if "id" not in request.session:
        request.session["id"] = 0
    return render(request, 'project_app/index.html')

def register(request):
    if "valid" not in request.session:
        request.session["valid"] = "Register"
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for error in errors.iteritems():
            messages.error(request, error)
        return redirect('/')
    else:
        new = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = request.POST['password'])
        print new
        request.session["id"] = new.id
        return redirect('/success')

def login(request):
    if "valid" not in request.session:
        request.session["valid"] = "Login"
    request.session["valid"] = "Login"
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for error in errors.itervalues():
            messages.error(request, error)
        return redirect('/')
    login_info = User.objects.get(email=request.POST['email'])
    if login_info == []:
        messages.error(request, "Invalid login credentials.")
        return redirect('/')
    elif len(errors):
        messages.error(request, "Invalid email or password")
        return redirect('/')
    else:
        hash = bcrypt.hashpw("request.POST['password']".encode(), bcrypt.gensalt())
        bcrypt.checkpw("request.POST['password']".encode(), hash)
        request.session['id'] = login_info.id
        return redirect('/success')

def success(request):
    if request.session['valid'] == "Register":
        messages.success(request, "You are registered!")

    id = request.session['id']
    user = User.objects.get(id = id)
    context = {
        # "name": User.objects.get(first_name=request.session['first_name']),
        "user": User.objects.get(id=request.session['id']),
        "all_items": Item.objects.filter(adder=request.session['id']),
        "other_items": Item.objects.exclude(adder=request.session['id']),
    }
    return render(request, "project_app/dash.html", context)

def item(request, id):
    context = {
        "item": Item.objects.get(id=int(id)),
        "users": User.objects.filter(others = Item.objects.get(id=int(id)))
    }
    return render(request, 'project_app/show.html', context)


def add(request, id):
    if request.method == 'POST':
        Item.objects.get(id=int(id)).users.add(User.objects.get(id=request.session['id']))
    return redirect('/success')

def create(request):
    return render(request, "project_app/create.html")

def remove(request,id):
    return redirect('/success')

def delete(request, id):
    Item.objects.get(id=int(id)).delete()
    return redirect('/success')

def new(request):
    errors = Item.objects.add_validator(request.POST)
    if len(errors):
        for error in errors .itervalues():
            messages.error(request, error)
        return redirect('/wish/create')
    else:
        new = Item.objects.create(adder=User.objects.get(id=request.session['id']), name = request.POST['name'])
        return redirect('/success')

def logout(request):
    request.session.pop('id')
    return redirect('/')
