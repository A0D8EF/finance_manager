from django.urls import path
from . import views

app_name = "finance"
urlpatterns = [
    path("", views.index, name="index"),

    path("income/", views.income, name="income"),
    path("income_list/", views.income_list, name="income_list"),
    path("add_expense_item/", views.expense_item, name="add_expense_item"),
]
