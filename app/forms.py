from django import forms
from .models import Transaction, Account


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['debit_account', 'credit_account', 'amount', 'description']

    def clean(self):
        cleaned_data = super().clean()
        debit = cleaned_data.get('debit_account')
        credit = cleaned_data.get('credit_account')
        amount = cleaned_data.get('amount')

        if debit == credit:
            raise forms.ValidationError("Счет дебета и кредита не могут совпадать.")
        if amount and amount <= 0:
            raise forms.ValidationError("Сумма должна быть больше нуля.")
        return cleaned_data
