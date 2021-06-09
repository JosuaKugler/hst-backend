import registration
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max
from django.core.mail import send_mail

from .models import Watchparty, User, Registration
from .forms import MainForm

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the registration index.")

def register(request, watchparty_loc_id):
    watchparty_list = get_list_or_404(Watchparty, loc_id=watchparty_loc_id) #get all watchpartys with watchparty_id
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MainForm(request.POST, watchparty_list=watchparty_list)
        # check whether it's valid:
        if form.is_valid():
            # deal with request.POST data here, see https://docs.djangoproject.com/en/3.2/intro/tutorial04/ for details
            # then redirect to successful registration page with validation email info
            # process the data in form.cleaned_data as required
            
            #create User:
            haushalt_id__max = max_haushalt_id()
            user = User(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                is_vaccinated = form.cleaned_data['is_vaccinated'],
                haushalt_id = haushalt_id__max + 1
            )
            user.save()

            # get all watchpartys the user registered for
            days = form.cleaned_data['days']
            watchpartys = list(Watchparty.objects.filter(loc_id = watchparty_list[0].loc_id))#all watchpartys with the location id
            
            selected_watchpartys = []
            for watchparty in watchpartys:
                print(watchparty.day.weekday())
                if str(watchparty.day.weekday()) in days:
                    selected_watchpartys.append(watchparty)

            #create registration objects
            for watchparty in selected_watchpartys:
                registration = Registration(
                    user = user,
                    watchparty = watchparty
                )
                registration.save()

            #do email stuff
            send_mail('Anmeldung Hochschultage Watchparty',)

            # redirect to a new URL:
            return HttpResponseRedirect('/registration/registration_success/' + str(user.id) + '/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MainForm(watchparty_list=watchparty_list)

    context = {'form': form, 'watchparty_list': watchparty_list}
    return render(request, 'registration/watchparty_registration.html', context)


def registration_success(request, user_id):
    user = get_object_or_404(User, id = user_id)
    registrations = Registration.objects.filter(user = user)
    watchparty_list = [registration.watchparty for registration in registrations]
    context = {'watchparty_list': watchparty_list}
    #deal with sending mail stuff here
    return render(request, 'registration/registration_success.html', context)

def validation_success(request):
    #link that user gets in email
    return HttpResponse("Hello, world. You're at the registration index.")

#helper function
def max_haushalt_id():
    return User.objects.all().aggregate(Max('haushalt_id'))['haushalt_id__max']


def send_validation_email(user, watchparty_list):
    subject = 'Anmeldung Hochschultage Watchparty'
    message = 'Hi' + user.firstname + ',\n'
    if len(watchparty_list) > 1:
        message += 'Du hast dich erfolgreich für folgende Watchpartys angemeldet:\n'
    else:
        message += 'Du hast dich erfolgreich für folgende Watchparty angemeldet:\n'
    
    for watchparty in watchparty_list:
        message += f'  - {watchparty.street}, {watchparty.plz} {watchparty.city} am {watchparty.day}\n'
    
    from_email = 'kontakt@hst-heidelberg.de'

    send_mail(subject, message, from_email, [user.email])