# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Activity
from ..login_app.models import User
from django.contrib import messages
import random


# Create your views here.

# Displays the page with the players with the five highest scores.
def highscores(request):
    if checkLogged(request) == False:
        return redirect('/')
    else:
        context = {
            "users": User.objects.all().order_by("-gold")[:5]
        }
        return render(request, "play_app/highscores.html", context)

# Displays the page for playing the game
def play(request):
    if checkLogged(request) == False:
        return redirect('/')
    else:
        context = {
            "activities": Activity.objects.filter(user_id = request.session["id"]).order_by("-created_at"),
            "user": User.objects.get(id = request.session["id"])
        }
        return render(request, "play_app/play.html", context)

# Manages the gold of the user when playing the game,
# deletes the user from the database and logs them out if the go under zero gold.
def process(request):
    user = User.objects.get(id = request.session["id"])
    # Gets a gold value for the user.
    if request.POST["building"] == "farm":
        gold = random.randrange(10, 21)
        location = "farm"
    elif request.POST["building"] == "cave":
        gold = random.randrange(5, 31)
        location = "cave"
    elif request.POST["building"] == "mountain":
        gold = random.randrange(15, 21)
        location = "mountain"
    elif request.POST["building"] == "casino":
        gold = random.randrange(-50, 51)
        location = "casino"

    # Adds or subtracts new gold.
    user.gold += gold
    user.save()

    # Determines phrasing for activity.
    if gold >= 0:
        profit = "earned"
    else:
        profit = "loss"

    # Creates new activity.
    activity = "You {} {} gold from the {} at".format(profit, abs(gold), location)
    newAct = Activity.objects.newAct(activity, user)

    # Deletes user if they have a negative gold amount
    if user.gold < 0:
        user.delete()
        messages.error(request, "You have been deleted from the game for losing all of your gold!")
        return redirect('/logout')

    return redirect('/game/play')

# Displays the all of users.
def dashboard(request):
    if checkLogged(request) == False:
        return redirect('/')
    else:
        context = {
            "users": User.objects.all(),
        }
        return render(request, "play_app/dashboard.html", context)

# Displays a user's page.
def userPage(request, id):
    if checkLogged(request) == False:
        return redirect('/')
    else:
        context = {
            "user": User.objects.get(id = id),
            "activities": Activity.objects.filter(user_id = id).order_by("-created_at"),
        }
        return render(request, "play_app/user.html", context)

# Checks to see if the user is logged in.
def checkLogged(request):
    try:
        request.session['loggedIn']
    except KeyError:
        request.session['loggedIn'] = False
    if not request.session['loggedIn']:
        messages.error(request, "Log in to view that page.")
    return request.session['loggedIn']