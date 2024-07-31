import spacy
from spacy.pipeline import EntityRuler
from spacy.language import Language
from storage.models import Tag

@Language.factory("create_entity_ruler")
def create_entity_ruler(nlp: Language, name: str):
    patterns = [
        {
            "label": "AMOUNT",
            "pattern": [
                {"LIKE_NUM": True},
                {"LOWER": {"IN": ["usd", "dollars", "$"]}, "OP": "?"},
            ],
        },
        {"label": "PERSON", "pattern": [{"POS": "PROPN"}, {"POS": "PROPN", "OP": "?"}]},
        {
            "label": "TRANSACTION_TYPE",
            "pattern": [
                {"LOWER": {"IN": ["payment", "transfer", "deposit", "withdrawal"]}}
            ],
        },
    ]

    ruler = EntityRuler(nlp, overwrite_ents=True)
    ruler.add_patterns(patterns)
    return ruler

try:
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("create_entity_ruler")
except Exception as e:
    print(f"Error loading spaCy model: {e}")
    nlp = None

def apply_tags_to_transaction(transaction):
    analysis = analyze_transaction(transaction.description)

    for tag_name in analysis['tags']:
        tag, _ = Tag.objects.get_or_create(tag=tag_name)
        transaction.tags.add(tag)

    transaction.save()       

def analyze_transaction(description):
    default_result = {
        "entities": [],
        "transaction_type": "Other",
        "person": None,
        "amount": None,
        "category": categorize_transaction(description, "Other"),
        "tags": [],
    }

    if nlp is None:
        print("NLP model not loaded. Using default categorization.")
        return default_result

    try:
        doc = nlp(description)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        transaction_type = next(
            (ent[0] for ent in entities if ent[1] == "TRANSACTION_TYPE"), "Other"
        )
        person = next((ent[0] for ent in entities if ent[1] == "PERSON"), None)
        amount = next((ent[0] for ent in entities if ent[1] == "AMOUNT"), None)

        category = categorize_transaction(description, transaction_type)

        analysis = {
            "entities": entities,
            "transaction_type": transaction_type,
            "person": person,
            "amount": amount,
            "category": category,
        }

        tags = generate_tags(analysis)
        analysis["tags"] = tags

        return analysis
    
    except Exception as e:
        print(f"Error analyzing transaction: {e}")
        return default_result


def categorize_transaction(description, transaction_type):
    description = description.lower()
    if "zelle" in description or "transfer" in description:
        return "Transfer"
    if transaction_type == "deposit" or "from" in description:
        return "Income"
    if transaction_type == "withdrawal" or transaction_type == "payment":
        return "Expense"

    return "Uncategorized"


def generate_tags(analysis):
    tags = []
    
    # Add category as a tag
    tags.append(analysis['category'])
    
    # Add transaction type as a tag if it's not "Other"
    if analysis['transaction_type'] != "Other":
        tags.append(analysis['transaction_type'])
    
    # Add person as a tag if present
    if analysis['person']:
        tags.append(f"Person: {analysis['person']}")
    
    # Add additional tags based on the description
    description = analysis['entities'][0][0] if analysis['entities'] else ""
    if "zelle" in description.lower():
        tags.append("Zelle")
    if "apple.com" in description.lower():
        tags.append("Apple")
    
    return tags

