from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from core.models import Player, Developer, User, Game

class SelectUserTypeForm(forms.Form):
    CHOICES = (
        ('1','player'),
        ('2','developer'),
    )
    select = forms.ChoiceField(widget=forms.Select, choices=CHOICES)


class PriceUpdateForm(forms.Form):
    new_price = forms.IntegerField(widget=forms.TextInput(attrs={'name': 'new_price'}))


class PlayerSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password confirmation'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    """@transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_player = True
        user.save()
        player = Player.objects.create(user=user)
        return user"""

class DeveloperSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password confirmation'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    """@transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_developer = True
        user.save()
        developer = Developer.objects.create(user=user)
        return user"""


class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('category', 'name', 'url', 'price', 'image', 'description')
