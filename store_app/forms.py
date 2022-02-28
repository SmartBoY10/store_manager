from django import forms

class AddToCartForm(forms.Form):
    cart_id = forms.IntegerField()
    quantity = forms.IntegerField()