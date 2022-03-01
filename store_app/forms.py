from django import forms

class AddToCartForm(forms.Form):
    cart_id = forms.IntegerField()
    quantity = forms.IntegerField()


class ConfirOrderForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    city = forms.CharField(max_length=50)
    pay_type = forms.IntegerField()