from django.db import models
from django.conf import settings
import json
import os
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    tag = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.tag


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    details = models.CharField(max_length=6)
    posting_date = models.DateField(db_index=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    check_or_slip = models.CharField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    structured_tags = models.JSONField(default=dict, blank=True)
    labels = models.JSONField(default=dict, blank=True)


    class Meta:
        unique_together = (
            "user",
            "details",
            "posting_date",
            "description",
            "amount",
            "transaction_type",
            "balance",
            "check_or_slip",
        )

    def analyze_description(self):
        from .transaction_analyzer import analyze_transaction
        analysis = analyze_transaction(self.description, self.user)
        for tag_name in analysis.get('tags', []):
            tag, _ = Tag.objects.get_or_create(tag=tag_name)
            self.tags.add(tag)
        self.labels = analysis.get('labels', {})
        self.save()

    @classmethod
    def reanalyze_all_for_user(cls, user):
        from .transaction_analyzer import apply_tags_to_transaction
        transactions = cls.objects.filter(user=user)
        for transaction in transactions:
            apply_tags_to_transaction(transaction)

class RuleBase(models.Model):
    LABEL_CHOICES = [
        ('Person', 'Person:'),
        ('Category', 'Category:'),
        ('Location', 'Location:'),
        ('Amount', 'Amount:'),
        ('Date', 'Date:'),
        ('Other', 'Other:'),
    ]
    name = models.CharField(max_length=100, unique=True)
    words = models.TextField()
    match_method = models.CharField(max_length=10, choices=[
        ('all', 'All words'),
        ('any', 'Any word'),
        ('exact', 'Exact phrase')
    ])
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=20, choices=LABEL_CHOICES, blank=True, null=True)
    metadata_key = models.CharField(max_length=100, blank=True, null=True)
    metadata_type = models.CharField(max_length=20, choices=[
        ('next_n_words', 'Next N Words'),
        ('regex', 'Regular Expression'),
        ('string_match', 'String Match')
    ], blank=True, null=True)
    metadata_value = models.CharField(max_length=100, blank=True, null=True)
    auto_tag = models.BooleanField(default=True, help_text="Automatically tag transactions with this label")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class AdminRules(RuleBase):

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        self.export_admin_tags()
        if is_new:
            for user in User.objects.all():
                Transaction.reanalyze_all_for_user(user)

    @classmethod
    def export_admin_tags(cls):
        json_file_path = os.path.join(settings.BASE_DIR, 'data', 'admin_tags.json')
        rules = cls.objects.all()
        data = []
        for rule in rules:
            data.append({
                'name': rule.name,
                'words': rule.words,
                'match_method': rule.match_method,
                'tag': rule.tag.tag if rule.tag else None,
                'label': rule.label,
                'metadata_type': rule.metadata_type,
                'metadata_value': rule.metadata_value,
                'auto_tag': rule.auto_tag,
            })
        
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)

    class Meta:
        verbose_name_plural = "Admin Rules"

class CustomRules(RuleBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            Transaction.reanalyze_all_for_user(self.user)

    class Meta:
        unique_together = ('name', 'user')
        verbose_name_plural = "Custom Rules"