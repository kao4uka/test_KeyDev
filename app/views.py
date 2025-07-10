from django.shortcuts import get_object_or_404, redirect
from django.views import generic, View
from django.urls import reverse_lazy

from .models import Account, Transaction
from .forms import TransactionForm


class AccountListView(generic.ListView):
    model = Account
    template_name = 'account_list.html'
    context_object_name = 'accounts'


class TransactionCreateView(generic.CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('transaction-list')


class TransactionListView(generic.ListView):
    model = Transaction
    template_name = 'transaction_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['original_transactions'] = Transaction.original_transactions()
        context['reversal_transactions'] = Transaction.reversal_transactions()
        return context


class TransactionReverseView(View):
    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        transaction.reverse()
        return redirect('transaction-list')
