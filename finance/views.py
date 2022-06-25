from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Balance
from .forms import BalanceForm

class IndexView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        context             = {}
        context["balances"] = Balance.objects.filter(user=request.user.id).order_by("-use_date")

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




