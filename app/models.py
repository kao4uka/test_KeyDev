import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class AccountType(models.TextChoices):
    ASSET = 'asset', _('Актив')
    LIABILITY = 'liability', _('Пассив')
    BOTH = 'both', _('Активно-пассивный')


class BalanceArticle(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BalanceGroup(models.Model):
    article = models.ForeignKey(BalanceArticle, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.article.name} / {self.name}"


class Account(models.Model):
    number = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=AccountType.choices)
    group = models.ForeignKey(BalanceGroup, on_delete=models.PROTECT, related_name='accounts')
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = str(uuid.uuid4().int)[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} - {self.name}"


class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0.01)])
    debit_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='debit_transactions')
    credit_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='credit_transactions')
    is_reversed = models.BooleanField(default=False)
    reversal_of = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reversals',
        verbose_name="Сторно для"
    )

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise ValueError("Сумма должна быть больше 0.")

        if self.debit_account == self.credit_account:
            raise ValueError("Дебит и Кредит счета должны быть разными.")

        if not self.pk:
            self._apply_double_entry()

        super().save(*args, **kwargs)

    def _apply_double_entry(self):
        debit_type = self.debit_account.type
        credit_type = self.credit_account.type

        if debit_type == AccountType.ASSET:
            self.debit_account.balance += self.amount
        elif debit_type == AccountType.LIABILITY:
            self.debit_account.balance -= self.amount

        if credit_type == AccountType.ASSET:
            self.credit_account.balance -= self.amount
        elif credit_type == AccountType.LIABILITY:
            self.credit_account.balance += self.amount

        self.debit_account.save()
        self.credit_account.save()

    def reverse(self):
        if self.is_reversed:
            raise ValueError("Transaction already reversed.")
        if self.reversal_of is not None:
            raise ValueError("Cannot reverse a reversal transaction.")

        reversed_transaction = Transaction.objects.create(
            description=f"Сторно транзакции #{self.pk}",
            amount=self.amount,
            debit_account=self.credit_account,
            credit_account=self.debit_account,
            reversal_of=self
        )
        self.is_reversed = True
        self.save()
        return reversed_transaction

    @staticmethod
    def original_transactions():
        return Transaction.objects.filter(reversal_of__isnull=True)

    @staticmethod
    def reversal_transactions():
        return Transaction.objects.filter(reversal_of__isnull=False)