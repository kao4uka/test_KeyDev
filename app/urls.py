from django.urls import path
from . import views

urlpatterns = [
    path('', views.AccountListView.as_view(), name='account-list'),
    path('transactions/history/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/create/', views.TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/reverse/', views.TransactionReverseView.as_view(), name='transaction-reverse'),
]
