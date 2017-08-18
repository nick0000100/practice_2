# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.

# Displays the login and registration page.
# User is redirected here if they try to access another page before being logged in
def index(request):
    return render(request, "login_app/index.html")

# Registers a new user with the given data, if it passes validation,
# if not then redirect to the homepage.
def register(request):
    errors = User.objects.validateReg(request.POST)
    if len(errors):
        # Redirects to start page.
        errorPrinter(request, errors)
        return redirect('/')
    else:
        # Create a new user and redirects to highscore page.
        user = User.objects.createUser(request.POST)
        loggedIn(request, user)
        return redirect('/game')

# Logs the user in and redirects to the highscore page if successful,
# if not redirect to the homepage.
def login(request):
    errors = User.objects.validateLogin(request.POST)
    if len(errors):
        # Redirects to start page.
        errorPrinter(request, errors)
        return redirect('/')
    else:
        # Redirects to highscore page.
        user = User.objects.get(email = request.POST["email"])
        loggedIn(request, user)
        return redirect('/game')

# Logs the user out and redirects them to the homepage.
def logout(request):
    request.session.flush()
    return redirect('/')


# Adds error messages to messages.
def errorPrinter(request, errors):
    for error, message in errors.iteritems():
        messages.error(request, message)

# Changes session data to that of the user's.
def loggedIn(request, user):
    try:
        request.session['loggedIn'] = True
    except KeyError:
        request.session['loggedIn']
    try:
        request.session["id"] = user.id
    except KeyError:
        request.session["id"]
    try:
        request.session["first_name"] = user.first_name
    except KeyError:
        request.session["first_name"]