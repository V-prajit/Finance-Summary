from storage.models import Tag, CustomRules, AdminRules
import re

def analyze_transaction(description, user):
    return {
        "tags": generate_tags(description, user),
    }

def generate_tags(description, user):
    tags = set()

    admin_rules = AdminRules.objects.all()
    for rule in admin_rules:
        if re.search(rule.pattern, description, re.IGNORECASE):
            tags.add(rule.tag.tag)

    user_rules = CustomRules.objects.filter(user=user)
    for rule in user_rules:
        if re.search(rule.pattern, description, re.IGNORECASE):
            tags.add(rule.tag.tag)
    
    return list(tags)

def apply_tags_to_transaction(transaction):
    analysis = analyze_transaction(transaction.description, transaction.user)
    for tag_name in analysis.get('tags', []):
        tag, _ = Tag.objects.get_or_create(tag=tag_name)
        transaction.tags.add(tag)
    transaction.save()