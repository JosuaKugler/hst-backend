from django import forms


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
        for i, watchparty in enumerate(self.watchparty_list):
            weekday = week[watchparty.day.weekday()]
            if watchparty in self.only_vaccinated_list:
                weekday = str(weekday) + " (nur für Geimpfte!)"
            newCHOICES.append((i, weekday))
        super(MainForm, self).__init__(*args, **kwargs)
        self.fields['days'].choices = newCHOICES

    CHOICES = [('1', 'Didnt work')]
    first_name = forms.CharField(label="Vorname", max_length=200)
    last_name = forms.CharField(label="Nachname", max_length=200)
    email = forms.EmailField(label="E-Mail-Adresse")
    address = forms.CharField(label="Adresse", max_length=200)
    is_vaccinated = forms.BooleanField(
        label="Geimpft oder Genesen?", required=False)
    wants_rapid_test = forms.BooleanField(
        label="Ich möchte vorher einen Selbsttest machen", required=False,
        help_text="Wir stellen dir Selbsttests zur Verfügung, sodass du dich direkt vor der Watchparty testen kannst."
        )
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=CHOICES, label="An welchen Tagen möchtest du teilnehmen?")


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
        for i, watchparty in enumerate(self.watchparty_list):
            weekday = week[watchparty.day.weekday()]
            if watchparty in self.only_vaccinated_list:
                weekday = str(weekday) + " (nur für Geimpfte!)"
            newCHOICES.append((i, weekday))
        super(MainForm, self).__init__(*args, **kwargs)
        self.fields['days'].choices = newCHOICES

    CHOICES = [('1', 'FATAL ERROR')]
    first_name = forms.CharField(label="Vorname", max_length=200)
    last_name = forms.CharField(label="Nachname", max_length=200)
    email = forms.EmailField(label="E-Mail-Adresse")
    #address = forms.CharField(label="Adresse", max_length=200)
    is_vaccinated = forms.BooleanField(
        label="Geimpft oder Genesen?", required=False)
    wants_rapid_test = forms.BooleanField(
        label="Ich möchte vorher einen Selbsttest machen", required=False,
        help_text="Wir stellen dir Selbsttests zur Verfügung, sodass du dich direkt vor der Watchparty testen kannst."
        )
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=CHOICES, label="An welchen Tagen möchtest du teilnehmen?")

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
    email = forms.EmailField(label="E-Mail-Adresse")
    
    plz = forms.CharField(max_length=5, label="Postleitzahl")
    city = forms.CharField(max_length=200, label="Stadt")
    street = forms.CharField(max_length=200, label="Straße, Hausnummer")
    # maximale Anzahl an Personen, die in die WG passen (inklusive Veranstalter-WG)
    max_place_num = forms.IntegerField(label="Wie viele Menschen passen in deine WG? (Inklusive dir und deinen Mitbewohnern)")
    wg_people_num = forms.IntegerField(label="Wie viele Menschen, die weder genesen noch geimpft sind, wohnen in deiner WG? (Wir brauchen die Info, um bei der Platzvergabe die Zahl an Haushalten/Personen korrekt berücksichtigen zu können")
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=CHOICES, label="An welchen Tagen möchtest du die Watchparty anbieten?")
