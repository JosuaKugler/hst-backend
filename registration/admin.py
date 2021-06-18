from django.contrib import admin

# Register your models here.
from .models import Household, User, Watchparty, Registration


class UserAdmin(admin.ModelAdmin):
    fields = [
        'first_name',
        'last_name',
        'email',
        'household',
        'is_vaccinated',
        'wants_rapid_test',
        'is_active',
        'creation_date',
        'token'
    ]
    list_display = ('first_name', 'last_name', 'email', 'creation_date', 'is_active')
    list_filter = [
        'is_active',
        'is_vaccinated',
        'wants_rapid_test',
        'creation_date',
        'household'
    ]
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'token'
    ]

class WatchpartyAdmin(admin.ModelAdmin):
    fields = [
        'loc_id',
        'plz',
        'city',
        'street',
        'day',
        'max_place_num',
        'wg_people_num',
        'first_name',
        'last_name',
        'email',
        'is_active',
        'is_confirmed',
        'creation_date',
        'token',
        'rapid_test',
        'latitude',
        'longitude'
    ]
    list_display = ('loc_id', 'first_name', 'last_name', 'rapid_test', 'is_confirmed')
    list_filter = ['rapid_test', 'is_confirmed', 'creation_date', 'loc_id']
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'token'
    ]

class RegistrationAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'watchparty',
        'creation_date'
    ]
    list_display = ('user', 'watchparty', 'creation_date')
    list_filter = [
        'user',
        'watchparty',
        'creation_date'
    ]
    search_fields = [
        'user',
        'watchparty',
        'creation_date'
    ]

class HouseholdAdmin(admin.ModelAdmin):
    fields = [
        'address',
        'token'
    ]
    list_display = ('address', 'token')
    list_filter = ['address']
    search_fields = ['token', 'address']


admin.site.register(User, UserAdmin)
admin.site.register(Watchparty, WatchpartyAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Household, HouseholdAdmin)