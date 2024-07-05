from django.db import models
from django.conf import settings

class Tag(models.Model):
    tag = models.CharField(max_length= 100, unique=True)

    def __str__(self):
        return self.tag

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    details = models.CharField(max_length = 6)
    posting_date = models.DateField(db_index=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits = 15, decimal_places=2)
    transaction_type = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits = 15, decimal_places=2)
    check_or_slip = models.CharField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    class Meta:
        unique_together = ('details', 'posting_date', 'description', 'amount', 'transaction_type', 'balance', 'check_or_slip')