from django import forms

# class PurchaseForm(forms.Form):
#     storage = forms.CharField(max_length=50)
#     product = forms.CharField(max_length=50)
#     quantity = forms.IntegerField()
#     price_per_unit = forms.IntegerField()

class PurchaseForm(forms.Form):
    storage = forms.CharField(max_length=55)
    product = forms.CharField(max_length=55)
    quantity = forms.IntegerField()
    price_per_unit = forms.IntegerField()