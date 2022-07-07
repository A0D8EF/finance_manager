from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ExpenseItem, Balance
from .forms import BalanceForm

class IndexView(LoginRequiredMixin, View):

    def monthly_calc(self, balances):

        data    = []

        for i in range(1,13):
            dic             = {}
            dic["month"]    = i
            dic["amount"]   = 0

            data.append(dic)
        
        for balance in balances:
            month   = balance.use_date.month
            income  = balance.expense_item.income
            amount  = balance.amount

            for d in data:
                if d["month"] != month:
                    continue
                
                if income:
                    d["amount"] += amount
                else:
                    d["amount"] -= amount
                
                break
        
        return data


    def get(self, request, *args, **kwargs):

        context                     = {}
        context["expense_items"]    = ExpenseItem.objects.filter(user=request.user.id)
        context["balances"]         = Balance.objects.filter(user=request.user.id).order_by("-use_date")

        context["monthly_balances"] = self.monthly_calc( Balance.objects.filter(user=request.user.id, use_date__year=2022).order_by("-use_date"))
        # models.DateField のフィールド名に __year で年を取り出す
        # TODO: ユーザーが入力した年（カレンダーで選択されている月？）の集計をできるように

        return render(request, "finance/index.html", context)
    

    def post(self, request, *args, **kwargs):
        
        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = BalanceForm(copied)

        if not form.is_valid():
            print("バリデーションNG")
            print(form.errors)
            return redirect("finance:index")

        print("バリデーションOK")
        form.save()

        return redirect("finance:index")


index = IndexView.as_view()




