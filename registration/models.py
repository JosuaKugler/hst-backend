from enum import unique
from django.db import models

# Create your models here.


class Household(models.Model):
    token = models.CharField(max_length=200)
    address = models.CharField(max_length=200)


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    is_vaccinated = models.BooleanField()
    wants_rapid_test = models.BooleanField()
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    is_active = models.BooleanField()
    creation_date = models.DateTimeField()
    token = models.CharField(max_length=200)


class Watchparty(models.Model):
    loc_id = models.IntegerField()  # watchpartys at the same place get the same id
    # address
    plz = models.CharField(max_length=5)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    day = models.DateField(max_length=200)
    # maximale Anzahl an Personen, die zusätzlich in die WG passen (ohne Veranstalter-WG)
    max_place_num = models.IntegerField()
    # Anzahl der Personen in der Veranstalter-WG ohne geimpfte
    wg_people_num = models.IntegerField()
    # host info
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    is_active = models.BooleanField()
    is_confirmed = models.BooleanField()
    creation_date = models.DateTimeField()
    token = models.CharField(max_length=200)
    rapid_test = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchparty = models.ForeignKey(Watchparty, on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    #constraints = [models.UniqueConstraint(fields=['user', 'watchparty'], name='unique_user_watchpary')]
