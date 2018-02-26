from django import forms

# Form to post gamestate to the game.
class GamestateForm(forms.Form):
    gameState = forms.CharField(required=True, widget=forms.HiddenInput)
