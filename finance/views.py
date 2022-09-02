from django.shortcuts import render, redirect
# from django.views import View
from rest_framework.views import APIView as View

from allauth.account.admin import EmailAddress
from django.contrib.auth.mixins import AccessMixin

from django.db.models import Q
from django.db.models import Sum

from .models import ExpenseItem, Balance
from .forms import BalanceForm, IncomeForm, ExpenseItemForm, YearMonthForm

import datetime
from . import calender, calc

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
        context["balances"]         = Balance.objects.filter(user=request.user.id, use_date__year=selected_date.year, use_date__month=selected_date.month ).order_by("use_date")

        # context["monthly_balances"] = calc.monthly_calc( Balance.objects.filter(user=request.user.id, use_date__year=selected_date.year).order_by("-use_date"), selected_date )
        # context["daily_balances"]   = calc.daily_calc( Balance.objects.filter(user=request.user.id, use_date__year=selected_date.year, use_date__month=selected_date.month).order_by("-use_date") )
        # models.DateField のフィールド名に __year で年を取り出す

        context["calender"]       = calender.create_calender(selected_date.year, selected_date.month)


        monthly_balances    = []
        for i in range(0,12):
            dic             = {}
            year            = int(selected_date.year)
            month           = int(selected_date.month)-i
            if month < 1:
                year  = int(selected_date.year)-1
                month = 12 + month
            total_income    = Balance.objects.filter(user=request.user.id, use_date__year=year, use_date__month=month, expense_item__income=True).aggregate(Sum("amount"))
            total_spending  = Balance.objects.filter(user=request.user.id, use_date__year=year, use_date__month=month, expense_item__income=False).aggregate(Sum("amount"))

            if total_income["amount__sum"] == None:
                total_income["amount__sum"] = 0
            if total_spending["amount__sum"] == None:
                total_spending["amount__sum"] = 0
            
            dic["year"]     = year
            dic["month"]    = month
            dic["amount"]   = total_income["amount__sum"] - total_spending["amount__sum"]
            dic["income"]   = total_income["amount__sum"]
            dic["spending"] = total_spending["amount__sum"]

            monthly_balances.append(dic)
        monthly_balances.reverse()

        length  = len(monthly_balances)
        harf    = int(length / 2)

        context["monthly_balances_left"]    = []
        context["monthly_balances_right"]   = []
        for i in range(harf):
            context["monthly_balances_left"].append(monthly_balances[i])
        
        for i in range(harf, length):
            context["monthly_balances_right"].append(monthly_balances[i])

        context["monthly_balances"] = monthly_balances


        daily_balances      = []
        dt = datetime.date(selected_date.year, selected_date.month, 1)
        while True:
            dic             = {}
            total_income    = Balance.objects.filter(user=request.user.id, use_date__year=dt.year, use_date__month=dt.month, use_date__day=dt.day, expense_item__income=True).aggregate(Sum("amount"))
            total_spending  = Balance.objects.filter(user=request.user.id, use_date__year=dt.year, use_date__month=dt.month, use_date__day=dt.day, expense_item__income=False).aggregate(Sum("amount"))

            if total_income["amount__sum"] == None:
                total_income["amount__sum"] = 0
            if total_spending["amount__sum"] == None:
                total_spending["amount__sum"] = 0
            
            dic["day"]      = dt.day
            dic["amount"]   = total_income["amount__sum"] - total_spending["amount__sum"]

            daily_balances.append(dic)
            dt += datetime.timedelta(days=1)

            if selected_date.month != dt.month:
                break
        context["daily_balances"]   = daily_balances


        incomes     = []
        spendings   = []
        for expense_item in context["expense_items"]:
            query       = Q( user=request.user.id, use_date__year=selected_date.year, use_date__month=selected_date.month, expense_item=expense_item.id )
            balances    = Balance.objects.filter(query).aggregate(Sum("amount"))

            dic             = {}
            dic["label"]    = expense_item.name
            dic["amount"]   = balances["amount__sum"]

            if expense_item.income:
                incomes.append(dic)
            else:
                spendings.append(dic)
            
        context["monthly_incomes"]  = incomes
        context["monthly_spendings"] = spendings

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
