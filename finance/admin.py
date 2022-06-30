from django.contrib import admin

from .models import ExpenseItem, Balance

class ExpenseItemAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "income", "name"]

class BalanceAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "expense_item", "amount", "use_date"]

admin.site.register(Balance, BalanceAdmin)
admin.site.register(ExpenseItem, ExpenseItemAdmin)

