from rest_framework import serializers
from .models import Transaction, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag']

class TransactionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many = True, read_only = True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'details', 'posting_date', 'description', 'amount', 'transaction_type', 'balance', 'check_or_slip', 'tags']

class TransactionWithTagsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'description', 'tags']