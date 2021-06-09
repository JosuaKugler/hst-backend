from django.shortcuts import get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Watchparty
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
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/registration/registration_success/')
            #return HttpResponse("Hello, world. You're at the registration index.")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MainForm(watchparty_list=watchparty_list)

    context = {'form': form, 'watchparty_list': watchparty_list}
    return render(request, 'registration/watchparty_registration.html', context)


def registration_success(request):
    #deal with sending mail stuff here
    return HttpResponse("Hello, world. You're at the registration index.")

def validation_success(request):
    #link that user gets in email
    return HttpResponse("Hello, world. You're at the registration index.")

