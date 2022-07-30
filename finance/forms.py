from django import forms
from .models import Balance, ExpenseItem

from django.core.validators import MinValueValidator, MaxValueValidator

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


# 年月検索用バリデーションフォーム
class YearMonthForm(forms.Form):
    year    = forms.IntegerField()
    month   = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])

