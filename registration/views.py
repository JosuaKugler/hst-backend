from datetime import date, datetime
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.regex_helper import Choice
import hashlib
import random

from .models import Household, Watchparty, User, Registration
from .forms import MainForm, SameHouseholdForm, WatchpartyForm
from .tokens import account_activation_token
from registration import models

#corona-rules:
max_people = 10
max_households = 3

# Create your views here.
def index(request):
    W = Watchparty.objects.all().filter(is_active = True).filter(is_confirmed = True)
    loc_ids = list(set([x.loc_id for x in list(W)])) # get all unique location ids
    
    W_repr_list = [W.filter(loc_id = loc_id)[0] for loc_id in loc_ids] #Repräsentatensystem für Watchpartys/(gleiche location)

    loc_dict = {}
    for watchparty in W_repr_list:
        plzcity = f"{watchparty.plz} {watchparty.city}"
        domain = get_current_site(request).domain
        link = f"https://{domain}/registration/{watchparty.loc_id}/"
        popup_str = f"""<strong> {watchparty.plz} {watchparty.city} </strong><br>
            { watchparty.street } <br>
            <br>
            freie Haushalte: { get_free_households(watchparty) }<br>
            freie Plätze: { get_free_vaccinated(watchparty) } (davon bis zu { get_free_unvaccinated(watchparty) } verfügbar für nicht Geimpfte)
            """
        if (get_free_vaccinated(watchparty)) <= 0:
            popup_str += f"<br><a href=' { link } '>Anmeldung</a>"
            
        loc_dict[watchparty.loc_id] = {"plzcity": plzcity, "street": watchparty.street, "link": link, "popup_str": popup_str}

    domain = get_current_site(request).domain

    return render(request, 'registration/registration_index_map.html', context={'loc_dict': loc_dict, 'domain': domain})

def register(request, watchparty_loc_id):
    watchparty_list = get_list_or_404(Watchparty, loc_id=watchparty_loc_id) #get all watchpartys with watchparty_id
    if watchparty_list[0].is_active == False:
        return HttpResponse('Die Mailadresse des Watchparty-Gastgebers wurde noch nicht bestätigt.')
    if watchparty_list[0].is_confirmed == False:
        return HttpResponse('Die Watchparty wurde noch nicht freigegeben.')    
    
    new_watchparty_list = []
    only_vaccinated_list = []

    

    for watchparty in watchparty_list:
        if get_free_vaccinated(watchparty) > 0:
            new_watchparty_list.append(watchparty)
        if get_free_unvaccinated(watchparty) > 0:
            only_vaccinated_list.append(watchparty)

    watchparty_list = new_watchparty_list # others are not relevant, because they are full

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MainForm(request.POST, watchparty_list=watchparty_list, only_vaccinated_list=only_vaccinated_list)
        # check whether it's valid:
        if form.is_valid():
            # deal with request.POST data here, see https://docs.djangoproject.com/en/3.2/intro/tutorial04/ for details
            # then redirect to successful registration page with validation email info
            # process the data in form.cleaned_data as required
            
            
            #create User:
            address = form.cleaned_data['address']
            token_base = address + str(random.randint(100000,1000000))
            token = hashlib.sha256(bytes(token_base, 'utf-8')).hexdigest()

            household = Household(
                address = address,
                token = token
            )
            household.save()

            user = User(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                is_vaccinated = form.cleaned_data['is_vaccinated'],
                wants_rapid_test = form.cleaned_data['wants_rapid_test'],
                household = household,
                is_active = False,
                creation_date = datetime.today() #returns time
            )
            user.save()

            # get all watchpartys the user registered for
            days = form.cleaned_data['days']
            
            selected_watchpartys = []
            for watchparty in watchparty_list:
                #print(watchparty.day.weekday())
                if str(watchparty.day.weekday()) in days:
                    if not user.is_vaccinated: #if user isn't vaccinated, a selected watchparty musn't be only_vaccinated
                        if not (watchparty in only_vaccinated_list):
                            selected_watchpartys.append(watchparty)
                    else:
                        selected_watchpartys.append(watchparty)
            
            if not selected_watchpartys:
                return HttpResponse("Diese Watchparty ist nur für Geimpfte/Genesene noch verfügbar")

            #create registration objects
            for watchparty in selected_watchpartys:
                registration = Registration(
                    user = user,
                    watchparty = watchparty,
                    creation_date = datetime.today()
                )
                registration.save()

            #do email stuff
            domain = get_current_site(request).domain
            send_email_validation_email(user, domain, "activate")

            # redirect to a new URL:
            return HttpResponseRedirect('/registration/registration_success/' + str(user.id) + '/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MainForm(watchparty_list=watchparty_list, only_vaccinated_list=only_vaccinated_list)

    context = {'form': form, 'watchparty_list': watchparty_list}
    return render(request, 'registration/registration.html', context)

def register_with_household_id(request, household_pk_uidb64, token):
    try:
        household_pk = force_text(urlsafe_base64_decode(household_pk_uidb64))
        household = Household.objects.get(pk=household_pk)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        household = None 
    
    if household is None or str(household.token) != str(token):
        return HttpResponse("ERROR 101: Anmeldelink ist ungültig.")
    
    
    users = list(User.objects.filter(household=household))
    if len(users) == 0:
        return HttpResponse("ERROR 102: Anmeldelink ist ungültig.")
    
    repr_user = users[0]

    registrations = list(Registration.objects.filter(user=repr_user))
    if len(registrations) == 0:
        return HttpResponse("ERROR 103: Anmeldelink ist ungültig.")
    
    repr_registration = registrations[0]

    repr_watchparty = repr_registration.watchparty
    watchparty_loc_id = repr_watchparty.loc_id

    watchparty_list = get_list_or_404(Watchparty, loc_id=watchparty_loc_id) #get all watchpartys with watchparty_id
    if watchparty_list[0].is_active == False:
        return HttpResponse('ERROR 104: Die Mailadresse des Watchparty-Gastgebers wurde noch nicht bestätigt.')
    if watchparty_list[0].is_confirmed == False:
        return HttpResponse('ERROR 105: Die Watchparty wurde noch nicht freigegeben.')
    
    new_watchparty_list = []
    only_vaccinated_list = []

    for watchparty in watchparty_list:
        if get_free_vaccinated(watchparty) > 0:
            new_watchparty_list.append(watchparty)
            current_household_already_on_watchparty = False
            for registration in Registration.objects.filter(watchparty=watchparty):
                if household == registration.user.household:
                    current_household_already_on_watchparty = True
            if current_household_already_on_watchparty:
                free_households = get_free_households(watchparty) + 1
            else:
                free_households = get_free_households(watchparty)
            if free_households <= 0 or get_free_unvaccinated(watchparty, check_households=False) <= 0: #no unvaccinated can access
                only_vaccinated_list.append(watchparty)

    watchparty_list = new_watchparty_list # others are not relevant, because they are full

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SameHouseholdForm(request.POST, watchparty_list=watchparty_list, only_vaccinated_list=only_vaccinated_list)
        # check whether it's valid:
        if form.is_valid():
            # deal with request.POST data here, see https://docs.djangoproject.com/en/3.2/intro/tutorial04/ for details
            # then redirect to successful registration page with validation email info
            # process the data in form.cleaned_data as required
            

            #create User:
            user = User(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                is_vaccinated = form.cleaned_data['is_vaccinated'],
                wants_rapid_test = form.cleaned_data['wants_rapid_test'],
                household = household,
                creation_date = datetime.today(),
                is_active = False
            )
            user.save()

            # get all watchpartys the user registered for
            days = form.cleaned_data['days']
            
            selected_watchpartys = []
            for watchparty in watchparty_list:
                #print(watchparty.day.weekday())
                if str(watchparty.day.weekday()) in days:
                    if not user.is_vaccinated: #if user isn't vaccinated, a selected watchparty musn't be only_vaccinated
                        if not (watchparty in only_vaccinated_list):
                            selected_watchpartys.append(watchparty)
                    else:
                        selected_watchpartys.append(watchparty)
            
            if not selected_watchpartys:
                return HttpResponse("ERROR 106: Diese Watchparty ist nur für Geimpfte/Genesene noch verfügbar")

            #create registration objects
            for watchparty in selected_watchpartys:
                registration = Registration(
                    user = user,
                    watchparty = watchparty,
                    creation_date = datetime.today()
                )
                registration.save()

            #do email stuff
            domain = get_current_site(request).domain
            send_email_validation_email(user, domain, "activate")

            # redirect to a new URL:
            return HttpResponseRedirect('/registration/registration_success/' + str(user.id) + '/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SameHouseholdForm(watchparty_list=watchparty_list, only_vaccinated_list=only_vaccinated_list)

    context = {'form': form, 'watchparty_list': watchparty_list, 'household_pk_uidb64': household_pk_uidb64, 'token':token}
    return render(request, 'registration/registration_same_household.html', context)

def registration_success(request, user_id):
    user = get_object_or_404(User, id = user_id)
    registrations = Registration.objects.filter(user = user)
    watchparty_list = [registration.watchparty for registration in registrations]
    print(watchparty_list)
    context = {'watchparty_list': watchparty_list}
    return render(request, 'registration/registration_success.html', context)

def activate(request, uidb64, email_token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None 
    if user is not None and account_activation_token.check_token(user, email_token):
        user.is_active = True
        user.save()

        #calculate watchparty_list
        registrations = Registration.objects.filter(user = user)
        watchparty_list = [registration.watchparty for registration in registrations]
        domain = get_current_site(request).domain

        household = user.household
        household_pk = urlsafe_base64_encode(force_bytes(household.pk))
        household_token = household.token

        household_link = f"https://{domain}/registration/household/{household_pk}/{household_token}/"

        send_confirmation_email(user, watchparty_list, domain, household_link)
        context = {'watchparty_list': watchparty_list, 'household_link': household_link}
        return render(request, 'registration/activate.html', context)
    else:
        return HttpResponse('Aktivierungslink ungültig!')

def new_watchparty(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WatchpartyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # deal with request.POST data here, see https://docs.djangoproject.com/en/3.2/intro/tutorial04/ for details
            # then redirect to successful registration page with validation email info
            # process the data in form.cleaned_data as required
            
            #get all days
            daynumbers = form.cleaned_data['days']
            days = [date(year=2021, month=6, day=20 + int(i)) for i in daynumbers]

            #create Watchparty:
            loc_id__max = max_loc_id()
            for day in days:
                watchparty = Watchparty(
                    plz = form.cleaned_data['plz'],
                    city = form.cleaned_data['city'],
                    street = form.cleaned_data['street'],
                    day = day,
                    max_place_num = form.cleaned_data['max_place_num'],
                    wg_people_num = form.cleaned_data['wg_people_num'],
                    loc_id = loc_id__max + 1,
                    email = form.cleaned_data['email'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    is_active = False,
                    is_confirmed = False, 
                    creation_date = datetime.today()
                )
                watchparty.save()

            
            
            #do email stuff
            domain = get_current_site(request).domain
            repr_watchparty = Watchparty.objects.all().filter(loc_id = loc_id__max + 1)[0]
            send_email_validation_email(repr_watchparty, domain, "watchparty_activate")
            # redirect to a new URL:
            return HttpResponseRedirect('/registration/watchparty_registration_success/' + str(watchparty.loc_id) + '/')
            #return HttpResponse("Watchparty created")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = WatchpartyForm()

    context = {'form': form}
    return render(request, 'registration/new_watchparty.html', context)

def watchparty_registration_success(request, loc_id):
    watchparty_list = get_list_or_404(Watchparty, loc_id = loc_id)
    context = {'watchparty_list': watchparty_list}
    return render(request, 'registration/watchparty_registration_success.html', context)

def watchparty_activate(request, uidb64, email_token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        watchparty = Watchparty.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        watchparty = None

    if watchparty is not None and account_activation_token.check_token(watchparty, email_token):
        watchparty_list = get_list_or_404(Watchparty, loc_id = watchparty.loc_id)
        context = {'watchparty_list': watchparty_list}
        for watchparty in watchparty_list:
            watchparty.is_active = True
            watchparty.save()
        #send confirmation email 
        domain = get_current_site(request).domain
        send_watchparty_confirmation_email(watchparty_list, domain)
        return render(request, 'registration/watchparty_activate.html', context)
    else:
        return HttpResponse('Aktivierungslink ungültig!')

#helper functions
def max_haushalt_id():
    a = User.objects.all().aggregate(Max('haushalt_id'))['haushalt_id__max']
    if a:
        return a
    else:
        return 0

def max_loc_id():
    a = Watchparty.objects.all().aggregate(Max('loc_id'))['loc_id__max'] 
    if a:
        return a
    else:
        return 0


def send_email_validation_email(obj, domain, type_activate):
    subject = 'Bestätige deine Emailadresse'
    context = {
        'first_name': obj.first_name,
        'uid': urlsafe_base64_encode(force_bytes(obj.pk)),
        'token': account_activation_token.make_token(obj),
        'domain': domain,
        'type_activate': type_activate
    }
    message = render_to_string('registration/email_validation_email_text.html', context)
    from_email = 'kontakt@hst-heidelberg.de'

    send_mail(subject, 
        message, 
        from_email, 
        [obj.email], 
        #html_message=htmlmessage, 
        fail_silently=False)

def send_confirmation_email(user, watchparty_list, domain, household_link):
    subject = 'Anmeldung Hochschultage Watchparty'
    context = {
        'user': user,
        'watchparty_list': watchparty_list,
        #'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #'token': account_activation_token.make_token(user),
        'domain': domain,
        'household_link': household_link,
    }
    #htmlmessage = render_to_string('registration/validation_email.html', context)
    message = render_to_string('registration/confirmation_email_text.html', context)
    from_email = 'kontakt@hst-heidelberg.de'

    send_mail(subject, 
        message, 
        from_email, 
        [user.email], 
        #html_message=htmlmessage, 
        fail_silently=False)


def send_watchparty_confirmation_email(watchparty_list, domain):
    subject = 'Hochschultage Watchparty Erstellen'
    repr_watchparty = watchparty_list[0]
    context = {
        'watchparty_list': watchparty_list,
        'first_name': repr_watchparty.first_name,
        #'uid': urlsafe_base64_encode(force_bytes(repr_watchparty.pk)),
        #'token': account_activation_token.make_token(repr_watchparty), #should also work with watchparty
        'domain': domain
    }
    #htmlmessage = render_to_string('registration/validation_email.html', context)
    message = render_to_string('registration/watchparty_confirmation_email_text.html', context)
    from_email = 'kontakt@hst-heidelberg.de'

    send_mail(subject, 
        message, 
        from_email, 
        [repr_watchparty.email], 
        #html_message=htmlmessage, 
        fail_silently=False)


def get_total_people(watchparty):
    registrations = Registration.objects.filter(watchparty=watchparty)
    cnt = 0
    for registration in registrations:
        #if registration.user.is_active:
        #    cnt += 1
        cnt += 1
    return cnt

def get_non_vaccined(watchparty):
    registrations = Registration.objects.filter(watchparty=watchparty)
    cnt = 0
    for registration in registrations:
        #if registration.user.is_active:
        #    if not registration.user.is_vaccinated:
        #        cnt += 1
        if not registration.user.is_vaccinated:
            cnt += 1
    return cnt

def get_households(watchparty):
    registrations = Registration.objects.filter(watchparty=watchparty)
    households = []
    for registration in registrations:
        #if registration.user.is_active:
        #    if not registration.user.is_vaccinated:
        #        if not registration.user.haushalt_id in households:
        #           households.append(registration.user.haushalt_id)
        if not registration.user.is_vaccinated:
            if not registration.user.household in households:
                households.append(registration.user.household)

    return len(households)


def get_free_households(watchparty):
    registrations = Registration.objects.filter(watchparty=watchparty)
    households = []
    for registration in registrations:
        #if registration.user.is_active:
        #    if not registration.user.is_vaccinated:
        #        if not registration.user.haushalt_id in households:
        #           households.append(registration.user.haushalt_id)
        if not registration.user.is_vaccinated:
            if not registration.user.household in households:
                households.append(registration.user.household)
    
    household_num = len(households)
    if watchparty.wg_people_num > 0:
        household_num = household_num + 1
    
    return max_households - household_num

def get_free_vaccinated(watchparty):
    registrations = Registration.objects.filter(watchparty=watchparty)
    cnt = 0
    for registration in registrations:
        #if registration.user.is_active:
        #    cnt += 1
        cnt += 1
    return watchparty.max_place_num - cnt


def get_free_unvaccinated(watchparty, check_households = True):
    if check_households:
        if get_free_households(watchparty) <= 0:
            return 0
    registrations = Registration.objects.filter(watchparty=watchparty)
    unvaccinated_cnt = 0
    for registration in registrations:
        #if registration.user.is_active:
        #    if not registration.user.is_vaccinated:
        #        cnt += 1
        if not registration.user.is_vaccinated:
            unvaccinated_cnt += 1
    
    unvaccinated_cnt += watchparty.wg_people_num
    free_unvaccinated_cnt = max_people - unvaccinated_cnt
    return min(get_free_vaccinated(watchparty), free_unvaccinated_cnt) #min( people that fit into the wg, people according to covid regulations)

