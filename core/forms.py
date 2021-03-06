from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from core.models import Player, Developer, User, Game

# Form for selection user type when signing up with a third party login
class SelectUserTypeForm(forms.Form):
    CHOICES = (
        ('player','Player'),
        ('developer','Developer'),
    )
    select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

# Form to update game price
class PriceUpdateForm(forms.Form):
    new_price = forms.IntegerField(widget=forms.TextInput(attrs={'name': 'new_price'}))

# Form for player signup.
class PlayerSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password confirmation'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# Form for developer signup.
class DeveloperSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password confirmation'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        

# Form for adding a new game.
class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('category', 'name', 'url', 'price', 'image', 'description')
