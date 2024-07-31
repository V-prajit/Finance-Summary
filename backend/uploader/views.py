from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import csv
from datetime import datetime
from storage.models import Transaction
from decimal import Decimal
import logging
from django.db import IntegrityError, transaction as db_transaction
from storage.transaction_analyzer import apply_tags_to_transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
logger = logging.getLogger(__name__)

# Create your views here.
ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS


@csrf_exempt
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_file(request):
    if "file" not in request.FILES:
        return JsonResponse({"error": "No File Uploaded"}, status=400)
    file = request.FILES["file"]
    if not allowed_file(file.name):
        return JsonResponse({"error": "File Extension Not Allowed"}, status=400)

    file_path = default_storage.save(file.name, file)
    transactions_added = 0
    errors = 0
    duplicates = 0

    try:
        with default_storage.open(file_path, "rt") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                try:
                    # Normalize and clean data
                    posting_date = datetime.strptime(
                        row["Posting Date"].strip(), "%m/%d/%Y"
                    ).date()
                    description = row["Description"].strip().lower()
                    details = row["Details"].strip()
                    amount = Decimal(row["Amount"].strip())
                    transaction_type = row["Type"].strip()
                    balance = Decimal(row["Balance"].strip())
                    check_or_slip = row.get("Check or Slip #", "").strip()

                    with db_transaction.atomic():
                        transaction_obj, created = Transaction.objects.get_or_create(
                            user=request.user,
                            details=details,
                            posting_date=posting_date,
                            description=description,
                            amount=amount,
                            transaction_type=transaction_type,
                            balance=balance,
                            check_or_slip=check_or_slip,
                        )
                        if created:
                            apply_tags_to_transaction(transaction_obj)
                            transactions_added += 1
                        else:
                            duplicates += 1
                except IntegrityError as e:
                    errors += 1
                    logger.error(
                        f"IntegrityError for transaction on {row['Posting Date']} with description {row['Description']}. Error: {str(e)}"
                    )
                except Exception as e:
                    errors += 1
                    logger.error(f"Error processing row: {row}. Error: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return JsonResponse({"error": "Error processing file"}, status=500)
    finally:
        default_storage.delete(file_path)

    return JsonResponse(
        {
            "message": "File Uploaded and processed successfully",
            "transactions_added": transactions_added,
            "errors": errors,
            "duplicates": duplicates,
        },
        status=200,
    )
