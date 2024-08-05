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
        fields = ['id', 'details', 'posting_date', 'description', 'amount', 'transaction_type', 'balance', 'check_or_slip', 'tags', 'structured_tags']

class TransactionWithTagsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'description', 'tags', 'structured_tags']

class RuleSerializer(serializers.ModelSerializer):
    label_display = serializers.CharField(source='get_label_display', read_only=True)
    tag = serializers.CharField()
    class Meta:
        fields = ['id', 'name', 'words', 'match_method', 'tag', 'label', 'label_display', 'metadata_type', 'metadata_value', 'auto_tag']


    def validate_tag(self, value):
        tag, created = Tag.objects.get_or_create(tag=value)
        return tag

class AdminRulesSerializer(RuleSerializer):
    class Meta(RuleSerializer.Meta):
        model = AdminRules

    def create(self, validated_data):
        tag = validated_data.pop('tag')
        instance = AdminRules.objects.create(tag=tag, **validated_data)
        AdminRules.export_admin_tags()
        return instance

    def update(self, instance, validated_data):
        if 'tag' in validated_data:
            tag = validated_data.pop('tag')
            instance.tag = tag
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        AdminRules.export_admin_tags()
        return instance

class CustomRulesSerializer(RuleSerializer):
    class Meta(RuleSerializer.Meta):
        model = CustomRules
        fields = RuleSerializer.Meta.fields + ['user']
        read_only_fields = ['user']

    def create(self, validated_data):
        tag = validated_data.pop('tag')
        validated_data['user'] = self.context['request'].user
        instance = CustomRules.objects.create(tag=tag, **validated_data)
        return instance

    def update(self, instance, validated_data):
        if 'tag' in validated_data:
            tag = validated_data.pop('tag')
            instance.tag = tag
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance