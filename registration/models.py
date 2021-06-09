from enum import unique
from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    is_vaccinated = models.BooleanField()
    haushalt_id = models.IntegerField()
    
class Watchparty(models.Model):
    loc_id = models.IntegerField() #watchpartys at the same place get the same id
    #adress
    plz = models.CharField(max_length=5)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    day = models.DateField(max_length=200)
    max_place_num = models.IntegerField() #maximale Anzahl an Personen, die in die WG passen (inklusive Veranstalter-WG)
    wg_people_num = models.IntegerField() #Anzahl der Personen in der Veranstalter-WG

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchparty = models.ForeignKey(Watchparty, on_delete=models.CASCADE)
    #constraints = [models.UniqueConstraint(fields=['user', 'watchparty'], name='unique_user_watchpary')]

