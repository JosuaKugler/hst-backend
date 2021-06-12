from django import forms

class MainForm(forms.Form):
    #pass attrs to add classes or styling to the fields
    def __init__(self,*args,**kwargs):
        #get watchparty_list in order to display selectable watchparty days
        self.watchparty_list = kwargs.pop('watchparty_list')
        newCHOICES = []
        week   = [ 
            'Montag', 
            'Dienstag', 
            'Mittwoch', 
            'Donnerstag',  
            'Freitag', 
            'Samstag',
            'Sonntag']
        for i, watchparty in enumerate(self.watchparty_list):
            weekday = week[watchparty.day.weekday()]
            newCHOICES.append((i, weekday))
        super(MainForm,self).__init__(*args,**kwargs)
        self.fields['days'].choices = newCHOICES

    CHOICES = [('1', 'Didnt work')]
    first_name = forms.CharField(label="Vorname", max_length=200)
    last_name = forms.CharField(label="Nachname", max_length=200)
    email = forms.EmailField(label="E-Mail-Adresse")
    address = forms.CharField(label="Adresse", max_length=200)
    is_vaccinated = forms.BooleanField(label="Geimpft oder Genesen?", required=False)
    wants_rapid_test = forms.BooleanField(label="Ich möchte vorher einen Schnelltest machen:", required=False)
    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES, label="An welchen Tagen möchtest du teilnehmen?")
