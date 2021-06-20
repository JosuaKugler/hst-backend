from django import forms
from geopy import Nominatim

class MainForm(forms.Form):
    # pass attrs to add classes or styling to the fields
    def __init__(self, *args, **kwargs):
        # get watchparty_list in order to display selectable watchparty days
        self.watchparty_list = kwargs.pop('watchparty_list')
        self.only_vaccinated_list = kwargs.pop('only_vaccinated_list')
        newCHOICES = []
        week = [
            'Montag',
            'Dienstag',
            'Mittwoch',
            'Donnerstag',
            'Freitag',
            'Samstag',
            'Sonntag']
        for watchparty in self.watchparty_list:
            weekday = week[watchparty.day.weekday()]
            if watchparty in self.only_vaccinated_list:
                weekday = str(weekday) + " (nur für Geimpfte!)"
            newCHOICES.append((watchparty.day.weekday(), weekday))
        super(MainForm, self).__init__(*args, **kwargs)
        self.fields['days'].choices = newCHOICES
    
    CHOICES = [('1', 'Didnt work')]
    first_name = forms.CharField(label="Vorname", max_length=200)
    last_name = forms.CharField(label="Nachname", max_length=200)
    email = forms.EmailField(label="E-Mail-Adresse", max_length=200)
    address = forms.CharField(label="Adresse", max_length=200)
    is_vaccinated = forms.BooleanField(
        label="Geimpft oder Genesen?", required=False)
    #wants_rapid_test = forms.BooleanField(
    #    label="Ich möchte vorher einen Selbsttest machen", required=False,
    #    help_text="Wir stellen dir Selbsttests zur Verfügung, sodass du dich direkt vor der Watchparty testen kannst."
    #    )
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=CHOICES, label="An welchen Tagen möchtest du teilnehmen?")
    data_consent = forms.BooleanField(label="Ich habe die Datenschutzerklärung gelesen und stimme auf dieser Grundlage der Verarbeitung meiner Daten zu.  Name und Email-Adresse werden an den Host der Watchparty weitergegeben.")

class SameHouseholdForm(forms.Form):
    # pass attrs to add classes or styling to the fields
    def __init__(self, *args, **kwargs):
        # get watchparty_list in order to display selectable watchparty days
        self.watchparty_list = kwargs.pop('watchparty_list')
        self.only_vaccinated_list = kwargs.pop('only_vaccinated_list')
        newCHOICES = []
        week = [
            'Montag',
            'Dienstag',
            'Mittwoch',
            'Donnerstag',
            'Freitag',
            'Samstag',
            'Sonntag']
        for watchparty in self.watchparty_list:
            weekday = week[watchparty.day.weekday()]
            if watchparty in self.only_vaccinated_list:
                weekday = str(weekday) + " (nur für Geimpfte!)"
            newCHOICES.append((watchparty.day.weekday(), weekday))
        super(SameHouseholdForm, self).__init__(*args, **kwargs)
        self.fields['days'].choices = newCHOICES

    CHOICES = [('1', 'FATAL ERROR')]
    first_name = forms.CharField(label="Vorname", max_length=200)
    last_name = forms.CharField(label="Nachname", max_length=200)
    email = forms.EmailField(label="E-Mail-Adresse", max_length=200)
    #address = forms.CharField(label="Adresse", max_length=200)
    is_vaccinated = forms.BooleanField(
        label="Geimpft oder Genesen?", required=False)
    #wants_rapid_test = forms.BooleanField(
    #    label="Ich möchte vorher einen Selbsttest machen", required=False,
    #    help_text="Wir stellen dir Selbsttests zur Verfügung, sodass du dich direkt vor der Watchparty testen kannst."
    #    )
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=CHOICES, label="An welchen Tagen möchtest du teilnehmen?")
    data_consent = forms.BooleanField(label="Ich habe die Datenschutzerklärung gelesen und stimme auf dieser Grundlage der Verarbeitung meiner Daten zu. Name und Email-Adresse werden an den Host der Watchparty weitergegeben.")

class WatchpartyForm(forms.Form):
    CHOICES = [
        ('1', 'Montag, 21.06.2021'),
        ('2', 'Dienstag, 22.06.2021'),
        ('3', 'Mittwoch, 23.06.2021'),
        ('4', 'Donnerstag, 24.06.2021'),
        ('5', 'Freitag, 25.06.2021'),
        ('6', 'Samstag, 26.06.2021'),
    ]
    first_name = forms.CharField(label="Vorname", max_length=200)
    last_name = forms.CharField(label="Nachname", max_length=200)
    email = forms.EmailField(label="E-Mail-Adresse", max_length=200, help_text="Vorname, Nachname und Email werden an die Teilnehmer der Watchparty weitergegeben.")
    
    plz = forms.CharField(max_length=5, label="Postleitzahl")
    city = forms.CharField(max_length=200, label="Stadt")
    street = forms.CharField(max_length=200, label="Straße, Hausnummer")
    # maximale Anzahl an Personen, die in die WG passen (inklusive Veranstalter-WG)
    rapid_test = forms.BooleanField(label="Ich möchte meinen Gästen Selbsttests anbieten (werden von den Hochschultagen gestellt).", required=False)
    max_place_num = forms.IntegerField(min_value="1", max_value="1000000", label="Wie viele Menschen möchtest du höchstens einladen?")
    wg_people_num = forms.IntegerField(min_value="1", max_value="1000000", label="Wie viele Menschen, die weder genesen noch geimpft sind, wohnen in deiner WG? (Wir brauchen die Info, um bei der Platzvergabe die Zahl an Haushalten/Personen korrekt berücksichtigen zu können)")
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=CHOICES, label="An welchen Tagen möchtest du die Watchparty anbieten?")
    
    data_consent = forms.BooleanField(label="Ich habe die Datenschutzerklärung gelesen und stimme auf dieser Grundlage der Verarbeitung meiner Daten zu. Insbesondere wird meine Adresse auf der Karte angezeigt sowie mein Name und meine Emailadresse an die Teilnehmer der Watchparty weitergegeben.")

    def clean(self):
        super().clean()

        if self.cleaned_data['max_place_num'] <= 0:
            self.add_error('max_place_num', 'Bitte gib eine positive Anzahl an Personen an.')
        
        if self.cleaned_data['wg_people_num'] <= 0:
            self.add_error('wg_people_num', 'Bitte gib eine positive Anzahl an Personen an.')
        
        plz = self.cleaned_data['plz']
        city = self.cleaned_data['city']
        street = self.cleaned_data['street']

        geolocator = Nominatim(user_agent="hst")
        location = geolocator.geocode(street + " " + plz + " " + city)
        if not location:
            msg = "Adresse konnte nicht gefunden werden. Sollte die Adresse korrekt sein, schreib uns gern eine Mail an kontakt@hst-heidelberg.de."
            self.add_error('plz', msg)
            self.add_error('city', msg)
            self.add_error('street', msg)
        else:
            self.cleaned_data['longitude'] = str(location.longitude)
            self.cleaned_data['latitude'] = str(location.latitude)

        return self.cleaned_data

class EditForm(forms.Form):
    # pass attrs to add classes or styling to the fields
    def __init__(self, *args, **kwargs):
        # get watchparty_list in order to display selectable watchparty days
        self.registered_list = kwargs.pop('registered_list')
        self.available_list = kwargs.pop('available_list')
        newCHOICES = []
        week = [
            'Montag',
            'Dienstag',
            'Mittwoch',
            'Donnerstag',
            'Freitag',
            'Samstag',
            'Sonntag']
        for watchparty in self.available_list:
            weekday = week[watchparty.day.weekday()]
            newCHOICES.append((watchparty.day.weekday(), weekday))
        
        for watchparty in self.registered_list:
            weekday = week[watchparty.day.weekday()]
            element = (watchparty.day.weekday(), weekday)
            if element not in newCHOICES:
                newCHOICES.append(element)
        
        newCHOICES.sort(key= (lambda tupel : tupel[0]))

        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['days'].choices = newCHOICES

    def get_initial_for_field(self, field: forms.MultipleChoiceField, field_name: str):
        #override
        initial = super().get_initial_for_field(field, field_name)
        print(initial)
        return initial
    
    CHOICES = [('1', 'Didnt work')]
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=CHOICES, label="An welchen Tagen möchtest du teilnehmen?", required=False)
