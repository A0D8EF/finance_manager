from django import forms
from .models import Balance, ExpenseItem

class BalanceForm(forms.ModelForm):

    class Meta:
        model   = Balance
        fields  = [ "user", "expense_item", "amount", "use_date", "description" ]


class ExpenseItemForm(forms.ModelForm):

    class Meta:
        model   = ExpenseItem
        fields  = ["user", "income", "name"]
    

# 費目選択肢バリデーション用(?income=trueが正常値であるか確認)
class IncomeForm(forms.ModelForm):

    class Meta:
        model   = ExpenseItem
        fields  = ["income"]
