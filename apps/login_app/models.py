# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

# Create your models here.

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):

    # Validates if the given information is acceptable to create a new user.
    def validateReg(self, postData):
        errors = {}
        first_name = postData["first_name"]
        last_name = postData["last_name"]
        email = postData["email"]
        password = postData["password"]
        cPass = postData["cPass"]

        # Validates the name of the user.
        if len(first_name) < 2:
            errors['first_name'] = "First name mush be at least 2 characters long."
        elif not NAME_REGEX.match(first_name):
            errors['first_name'] = "First must only contain letters"
        if len(last_name) < 2:
            errors['last_name'] = "Last name mush be at least 2 characters long."
        elif not NAME_REGEX.match(last_name):
            errors['last_name'] = "Last name must only contain letters"

        # Validates the given email based on length, if it is a correctly formated email, and if it already exist in the database.
        if len(email) <= 0:
            errors["email"] = "Email is required"
        elif not EMAIL_REGEX.match(email):
            errors["email"] = "Not a valid email"
        else:
            if len(User.objects.filter(email=postData["email"])) > 0:
                errors["email"] = "Email already exist in database"

        # Validates the given password from the user.
        if len(password) < 8:
            errors['password'] = "Password is not long enough."
        elif password != cPass:
            errors["password"] = "Password and password confirmation did not match."

        return errors

    # Validates the given information to see if the user is able to login.
    def validateLogin(self, postData):
        errors = {}
        email = postData['email']
        password = postData['password']
        user = User.objects.filter(email = email)
        if len(user) != 1:
            errors["email"] = "Email does not exist in the database."
        else:
            if not bcrypt.checkpw(password.encode(), user[0].password.encode()):
                errors["password"] = "Incorrect username/password combination."
        return errors
    
    # Creats a new user.
    def createUser(self, postData):
        first_name = postData["first_name"]
        last_name = postData["last_name"]
        email = postData["email"]
        password = postData["password"]
        hashPass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = first_name,
                            last_name = last_name,
                            email = email,
                            password = hashPass,
                            gold = 0
        )

        return user

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    gold = models.IntegerField()
    objects = UserManager()