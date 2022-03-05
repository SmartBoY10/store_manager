from django import forms


class PurchaseForm(forms.Form):
    storage = forms.CharField(max_length=55)
    product = forms.CharField(max_length=55)
    quantity = forms.IntegerField()
    price_per_unit = forms.IntegerField()


class SaleForm(forms.Form):
    storage = forms.CharField(max_length=55)
    product = forms.CharField(max_length=55)
    quantity = forms.IntegerField()
    price_per_unit = forms.IntegerField()