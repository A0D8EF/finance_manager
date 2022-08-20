from django.urls import path
from . import views

app_name = "finance"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.index, name="index_single"),

    path("income/", views.income, name="income"),
    path("income_list/", views.income_list, name="income_list"),
    # path("delete/<int:pk>/", views.delete, name="delete"),
    # path("edit/<int:pk>/", views.edit, name="edit"),
]
