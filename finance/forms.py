from django import forms
from .models import Balance

class BalanceForm(forms.ModelForm):

    class Meta:
        model   = Balance
        fields  = [ "user", "expense_item", "amount", "use_date", "description" ]

