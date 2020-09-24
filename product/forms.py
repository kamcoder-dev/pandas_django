from django import forms
from .models import Purchase, Product


class PurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                     label='Product',)

    class Meta:
        model = Purchase
        fields = ['product', 'price', 'quantity']
