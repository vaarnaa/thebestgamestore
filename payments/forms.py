from django import forms

# Form for posting payment details to third party payment service.
class PaymentForm(forms.Form):
    pid = forms.CharField(required=True, widget=forms.HiddenInput)
    sid = forms.CharField(required=True, widget=forms.HiddenInput)
    amount = forms.CharField(required=True, widget=forms.HiddenInput)
    success_url = forms.CharField(required=True, widget=forms.HiddenInput)
    cancel_url = forms.CharField(required=True, widget=forms.HiddenInput)
    error_url = forms.CharField(required=True, widget=forms.HiddenInput)
    checksum = forms.CharField(required=True, widget=forms.HiddenInput)
