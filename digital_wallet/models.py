from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _

User = get_user_model()


class Wallet(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = _('wallet')
        verbose_name_plural = _('wallets')

    def __str__(self):
        return f"{self.user} > {self.balance}"


class BaseTransaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2 ,verbose_name=_('Amount'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))

    class Meta:
        abstract = True


class Transaction(BaseTransaction):
    TRANSACTION_TYPES = (
        ('D', 'Deposit'),
        ('W', 'Withdraw'),
        ('T', 'Transfer'),
    )

    sender = models.ForeignKey(User, verbose_name=_('Sender'), on_delete=models.CASCADE, related_name='sent')
    recipient = models.ForeignKey(User, verbose_name=_('Receiver'), on_delete=models.CASCADE, related_name='received')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')

    def __str__(self):
        return f"{self.sender} > {self.recipient}"


class Deposit(BaseTransaction):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='deposits')

    class Meta:
        verbose_name = _('deposit')
        verbose_name_plural = _('deposits')


class Withdraw(BaseTransaction):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='withdraws')

    class Meta:
        verbose_name = _('withdraw')
        verbose_name_plural = _('withdraws')
