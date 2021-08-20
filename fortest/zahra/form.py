from django import forms


class Add(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)
