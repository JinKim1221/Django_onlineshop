from django import forms
# Forms ?
# it allows users to input information on client side
# it processes data that users input

class AddProductForm(forms.Form):
    quantity = forms.IntegerField()
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
