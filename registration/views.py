from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site

from .models import Watchparty, User, Registration
from .forms import MainForm
from .tokens import account_activation_token

# Create your views here.
def index(request):
    W = Watchparty.objects.all()
    loc_ids = list(set([x.loc_id for x in list(W)])) # get all unique location ids
    
    W_repr_list = [W.filter(loc_id = loc_id)[0] for loc_id in loc_ids] #Repräsentatensystem für Watchpartys/(gleiche location)

    loc_dict = {}
    for watchparty in W_repr_list:
        plzcity = f"{watchparty.plz} {watchparty.city}"
        domain = get_current_site(request).domain
        link = f"http://{domain}/registration/{watchparty.loc_id}/"
        loc_dict[watchparty.loc_id] = {"plzcity": plzcity, "street": watchparty.street, "link": link}

    return render(request, 'registration/registration_index_map.html', context={'loc_dict': loc_dict})

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
                wants_rapid_test = form.cleaned_data['wants_rapid_test'],
                address = form.cleaned_data['address'],
                haushalt_id = haushalt_id__max + 1,
                is_active = False
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
            domain = get_current_site(request).domain
            send_validation_email(user, selected_watchpartys, domain)

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
    return render(request, 'registration/registration_success.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Deine Anmeldung wurde bestätigt. Vielen Dank!')
    else:
        return HttpResponse('Aktivierungslink ungültig!')

def new_watchparty(request):
    return HttpResponse('Hier entsteht eine neue Watchparty')

#helper functions
def max_haushalt_id():
    return User.objects.all().aggregate(Max('haushalt_id'))['haushalt_id__max']


def send_validation_email(user, watchparty_list, domain):
    subject = 'Anmeldung Hochschultage Watchparty'
    context = {
        'user': user,
        'watchparty_list': watchparty_list,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'domain': domain
    }
    htmlmessage = render_to_string('registration/validation_email.html', context)
    message = render_to_string('registration/validation_email.html', context)
    from_email = 'kontakt@hst-heidelberg.de'

    send_mail(subject, 
        message, 
        from_email, 
        [user.email], 
        #html_message=htmlmessage, 
        fail_silently=False)