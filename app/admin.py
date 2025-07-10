from django.contrib import admin

from .models import Account, Transaction, BalanceArticle, BalanceGroup


admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(BalanceArticle)
admin.site.register(BalanceGroup)
