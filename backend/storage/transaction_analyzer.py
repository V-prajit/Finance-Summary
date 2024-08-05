from storage.models import Tag, CustomRules, AdminRules
import re

def analyze_transaction(description, user):
    tags, metadata = generate_tags(description, user)
    return {
        "tags": tags,
        "metadata": metadata,
    }

def generate_tags(description, user):
    tags = set()
    structured_tags = {}
    admin_rules = AdminRules.objects.all()
    user_rules = CustomRules.objects.filter(user=user)

    for rule in list(admin_rules) + list(user_rules):
        match, extracted_value = match_rule(rule, description)
        if match:
            if rule.label:
                label = rule.get_label_display().rstrip(':')
                structured_tags[label] = extracted_value
                if rule.auto_tag:
                    tags.add(f"{label}:Tagged")
            else:
                tags.add(rule.tag.tag)
            
            if extracted_value:
                tags.add(extracted_value)

    for label, value in structured_tags.items():
        if value.lower() in description.lower():
            tags.add(f"{label}:Tagged")

    return list(tags), structured_tags


def match_rule(rule, description):
    description_lower = description.lower()
    words = rule.words.lower().split()

    if rule.metadata_type == 'string_match':
        if rule.match_method == 'all':
            match = all(word in description_lower for word in words)
        elif rule.match_method == 'any':
            match = any(word in description_lower for word in words)
        elif rule.match_method == 'exact':
            match = rule.words.lower() in description_lower
        return match, rule.metadata_value if match else ''

    elif rule.metadata_type == 'next_n_words':
        if rule.words.lower() in description_lower:
            n = int(rule.metadata_value)
            words = description.split()
            start_index = ' '.join(words).lower().index(rule.words.lower()) + len(rule.words)
            relevant_words = words[start_index:start_index + n]
            return True, ' '.join(relevant_words)

    elif rule.metadata_type == 'regex':
        match = re.search(rule.words, description, re.IGNORECASE)
        if match:
            if rule.metadata_value:
                value_match = re.search(rule.metadata_value, description)
                if value_match:
                    return True, value_match.group(1) if value_match.groups() else value_match.group(0)
            return True, match.group(0)
    else:
        return False, ''

def apply_tags_to_transaction(transaction):
    tags, structured_tags = generate_tags(transaction.description, transaction.user)
    
    # Clear existing tags and re-apply
    transaction.tags.clear()
    for tag_name in tags:
        tag, _ = Tag.objects.get_or_create(tag=tag_name)
        transaction.tags.add(tag)
    
    transaction.structured_tags = structured_tags
    transaction.save()