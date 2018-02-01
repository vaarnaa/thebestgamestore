from django import forms


GAME_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddGameForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=GAME_QUANTITY_CHOICES,
                                      coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
