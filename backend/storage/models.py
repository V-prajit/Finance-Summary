from django.db import models
from django.conf import settings

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    details = models.CharField(max_length = 6)
    posting_date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits = 15, decimal_places=2)
    transaction_type = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits = 15, decimal_places=2)
    check_or_slip = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('details', 'posting_date', 'description', 'amount', 'transaction_type', 'balance', 'check_or_slip')