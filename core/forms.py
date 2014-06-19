from django import forms
from models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show

    name = forms.CharField(max_length=100)
    started = forms.DateInput()
    ended = forms.DateInput()
    thumbnail = forms.ImageField()
    networks = forms.ModelMultipleChoiceField(queryset=Network.objects.all())
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['networks'] = [n.pk for n in kwargs['instance'].networks.all()]
            initial['category'] = [c.pk for c in kwargs['instance'].categories.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['started'].widget.attrs.update({'readonly': '', 'data-date-format': 'dd-mm-yyyy'})
        self.fields['ended'].widget.attrs.update({'readonly': '', 'data-date-format': 'dd-mm-yyyy'})

    def save(self, commit=True):

        instance = forms.ModelForm.save(self)
        instance.categories.clear()
        instance.networks.clear()

        for category in self.cleaned_data['categories']:
            instance.categories.add(category)

        for network in self.cleaned_data['networks']:
            instance.networks.add(network)
        return super(ShowForm, self).save(commit)


class ShowAdminForm(forms.ModelForm):
    class Meta:
        model = Show

    name = forms.CharField(max_length=100)
    started = forms.DateInput()
    ended = forms.DateInput()
    thumbnail = forms.ImageField()
    networks = forms.ModelMultipleChoiceField(queryset=Network.objects.all())
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['networks'] = [n.pk for n in kwargs['instance'].networks.all()]
            initial['category'] = [c.pk for c in kwargs['instance'].categories.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):

        instance = forms.ModelForm.save(self)
        instance.categories.clear()
        instance.networks.clear()

        for category in self.cleaned_data['categories']:
            instance.categories.add(category)

        for network in self.cleaned_data['networks']:
            instance.networks.add(network)
        return super(ShowAdminForm, self).save(commit)


class CreateAccountForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CreateAccountForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user