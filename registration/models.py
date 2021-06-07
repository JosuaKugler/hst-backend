from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

class Watchparty(models.Model):
    #adress
    plz = models.CharField(max_length=5)
    city = models.CharField(max_length=200)
    