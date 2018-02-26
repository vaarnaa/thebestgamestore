from django import forms


class GamestateForm(forms.Form):
    gameState = forms.CharField(required=True, widget=forms.HiddenInput)
