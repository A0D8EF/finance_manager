from django.shortcuts import render, redirect
from django.views import View

from allauth.account.admin import EmailAddress
from django.contrib.auth.mixins import AccessMixin

from .models import ExpenseItem, Balance
from .forms import BalanceForm, IncomeForm, ExpenseItemForm, YearMonthForm

from . import calender

from django.http.response import JsonResponse
from django.template.loader import render_to_string

class LoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not EmailAddress.objects.filter(user=request.user.id, verified=True).exists():
            print("メールの確認が済んでいません")
            return redirect("account_email")

        return super().dispatch(request, *args, **kwargs)


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

        context             = {}
        context["months"]    = [ i for i in range(1,13) ]

        form    = YearMonthForm(request.GET)

        if form.is_valid():
            cleaned = form.clean()


        # context["expense_items"]    = ExpenseItem.objects.filter(user=request.user.id)
        context["balances"]         = Balance.objects.filter(user=request.user.id).order_by("-use_date")

        context["monthly_balances"] = self.monthly_calc( Balance.objects.filter(user=request.user.id, use_date__year=2022).order_by("-use_date"))
        # models.DateField のフィールド名に __year で年を取り出す
        # TODO: ユーザーが入力した年（カレンダーで選択されている月？）の集計をできるように

        context["calender"]       = calender.create_calender(2022, 7)

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


class IncomeView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        data    = { "error": True }

        form    = IncomeForm(request.GET)

        if not form.is_valid():
            print(form.errors)
            return JsonResponse(data)
        
        # 収入フラグの値をブーリアン値に変更する
        # request.GET["income"]で出てくるのは"true"という文字列
        cleaned     = form.clean()
        
        context     = {}
        context["expense_items"]    = ExpenseItem.objects.filter(user=request.user.id, income=cleaned["income"])

        data["error"]   = False
        # render_to_stringでレンダリング結果を文字列として返す
        data["content"] = render_to_string("finance/income.html", context, request)

        return JsonResponse(data)
        # data = { "error": False, "content": レンダリング結果の文字列 }
    
    def post(self, request, *args, **kwargs):

        data    = { "error": True }

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = ExpenseItemForm(copied)

        if not form.is_valid():
            print(form.errors)
            return JsonResponse(data)
        
        form.save()
        data["error"]   = False

        return JsonResponse(data)


income = IncomeView.as_view()


class ExpenseItemView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        context                 = {}
        context["expense_items"] = ExpenseItem.objects.filter(user=request.user.id)

        return render(request, "finance/add_expense_item.html", context)

    def post(self, request, *args, **kwargs):
        
        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = ExpenseItemForm(copied)

        if not form.is_valid():
            print("ExpenseItem: バリデーションNG")
            print(form.errors)
            return redirect("finance:income")

        print("ExpenseItem: バリデーションOK")
        form.save()

        return redirect("finance:index")


expense_item = ExpenseItemView.as_view()

