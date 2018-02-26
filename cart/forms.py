from django import forms


GAME_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 2)]

# Form for adding a game in the cart
class CartAddGameForm(forms.Form):
    quantity = 1
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
