from rest_framework import serializers
from .models import Transaction, Tag, CustomRules, AdminRules

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

class AdminRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRules
        fields = ['id', 'name', 'pattern', 'tag']

class CustomRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRules
        fields = ['id', 'name', 'pattern', 'tag', 'user']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)