from django.shortcuts import render, redirect
# from django.views import View
from rest_framework.views import APIView as View

from allauth.account.admin import EmailAddress
from django.contrib.auth.mixins import AccessMixin

from .models import ExpenseItem, Balance
from .forms import BalanceForm, IncomeForm, ExpenseItemForm, YearMonthForm

import datetime
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
            dic["income"]   = 0
            dic["spending"] = 0

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
                    d["income"] += amount
                else:
                    d["amount"] -= amount
                    d["spending"] += amount
                
                break
        
        return data


    def get(self, request, *args, **kwargs):

        context             = {}
        context["months"]    = [ i for i in range(1,13) ]

        form    = YearMonthForm(request.GET)
        today   = datetime.date.today()

        if form.is_valid():
            cleaned = form.clean()

            selected_date   = datetime.date(year=cleaned["year"], month=cleaned["month"], day=1)
        else:
            selected_date   = datetime.date(year=today.year, month=today.month, day=1)

        context["selected_date"] = selected_date

        context["years"]                                = calender.create_years(request, selected_date, today)
        context["next_month"], context["last_month"]    = calender.create_months(selected_date)
       
        context["expense_items"]    = ExpenseItem.objects.filter(user=request.user.id)
        context["balances"]         = Balance.objects.filter(user=request.user.id).order_by("use_date")

        context["monthly_balances"] = self.monthly_calc( Balance.objects.filter(user=request.user.id, use_date__year=selected_date.year).order_by("-use_date"))
        # models.DateField のフィールド名に __year で年を取り出す

        context["calender"]       = calender.create_calender(selected_date.year, selected_date.month)

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

    def delete(self, request, *args, **kwargs):
        
        data    = { "error": True }

        if "pk" not in kwargs:
            return JsonResponse(data)

        balance = Balance.objects.filter(user=request.user.id, id=kwargs["pk"]).first()
        if balance:
            balance.delete()
            data["error"] = False

        return JsonResponse(data)
    
    def put(self, request, *args, **kwargs):
        
        data    = { "error": True }

        if "pk" not in kwargs:
            return JsonResponse(data)

        balance         = Balance.objects.filter(user=request.user.id, id=kwargs["pk"]).first()

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form            = BalanceForm(copied, instance=balance)

        if not form.is_valid():
            print("バリデーションNG")
            print(form.errors)
            return JsonResponse(data)
        
        form.save()
        data["error"]   = False

        return JsonResponse(data)

        
    def patch(self, request, *args, **kwargs):
        pass


index = IndexView.as_view()

"""
class DeleteView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):

        data    = { "error": True }

        balance = Balance.objects.filter(user=request.user.id, id=pk).first()
        if balance:
            balance.delete()
            data["error"] = False

        return JsonResponse(data)

delete = DeleteView.as_view()

class EditView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):

        data    = { "error": True }
        
        context     = {}
        context["balance"]          = Balance.objects.filter(user=request.user.id, id=pk).first()
        context["expense_items"]    = ExpenseItem.objects.filter(user=request.user.id)

        data["error"]   = False
        data["content"] = render_to_string("finance/edit.html", context, request)

        return JsonResponse(data)

    def post(self, request, pk, *args, **kwargs):

        balance = Balance.objects.filter(user=request.user.id, id=pk).first()

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = BalanceForm(copied, instance=balance)

        if not form.is_valid():
            print("バリデーションNG")
            print(form.errors)
            return redirect("finance:index")
        
        form.save()

        return redirect("finance:index")
    
edit    = EditView.as_view()
"""

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


class IncomeListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        data    = { "error": True }

        form    = IncomeForm(request.GET)

        if not form.is_valid():
            print(form.errors)
            return JsonResponse(data)
        
        cleaned     = form.clean()
        
        context     = {}
        context["expense_items"]    = ExpenseItem.objects.filter(user=request.user.id)

        data["error"]   = False
        data["content"] = render_to_string("finance/income_list.html", context, request)

        return JsonResponse(data)

income_list = IncomeListView.as_view()
