from storage.models import Tag
import re

def analyze_transaction(description):
    return {
        "category": categorize_transaction(description),
        "tags": generate_tags(description),
    }

def categorize_transaction(description):
    return "Transfer" if "zelle" in description.lower() else None

import re

def generate_tags(description):
    tags = []
    description_lower = description.lower()

    # Foreign exchange rate adjustment fee
    if "foreign exchange rate adjustment fee" in description_lower:
        tags.append("Type: Foreign Exchange Fee")
        
        words = description_lower.split()
        excluded_words = set(["foreign", "exchange", "rate", "adjustment", "fee"])
        merchants = set(word.title() for word in words 
                        if word not in excluded_words 
                        and word.isalpha() 
                        and not re.match(r'\d{2}/\d{2}', word))
        
        if merchants:
            tags.append(f"Merchant: {' & '.join(merchants)}")
        
        tags.append("Category: Travel")

    # Zelle payments
    elif "zelle payment" in description_lower:
        tags.append("Type: Zelle Transfer")
        
        # Determine direction
        direction = "To" if "zelle payment to" in description_lower else "From"
        tags.append(f"Direction: {direction}")

        # Extract name using regex
        name_match = re.search(r'zelle payment (?:to|from)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)', description, re.IGNORECASE)
        if name_match:
            person_name = name_match.group(1).strip().title()
            tags.append(f"Person: {person_name}")

    return tags

def apply_tags_to_transaction(transaction):
    analysis = analyze_transaction(transaction.description)

    for tag_name in analysis.get('tags', []):
        tag, _ = Tag.objects.get_or_create(tag=tag_name)
        transaction.tags.add(tag)

    transaction.save()