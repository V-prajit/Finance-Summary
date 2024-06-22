from django.db import models

# Create your models here.
class Transaction(models.Model):
    details = models.CharField(max_length = 6)
    posting_date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits = 15, decimal_places=2)
    transaction_type = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits = 15, decimal_places=2)
    check_or_slip = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('details', 'posting_date', 'description', 'amount', 'transaction_type', 'balance', 'check_or_slip')