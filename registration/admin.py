from django.contrib import admin

# Register your models here.
from .models import Household, User, Watchparty, Registration

admin.site.register(User)
admin.site.register(Watchparty)
admin.site.register(Registration)
admin.site.register(Household)