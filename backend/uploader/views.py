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

logger = logging.getLogger(__name__)

# Create your views here.
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No File Uploaded'}, status=400)
        file = request.FILES['file']
        if not allowed_file(file.name):
            return JsonResponse({'error': 'File Extension Not Allowed'}, status=400)
        
        file_path = default_storage.save(file.name, file)
        transactions_added = 0
        errors = 0
        try:
            with default_storage.open(file_path, 'rt') as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    try:
                        # Normalize and clean data
                        posting_date = datetime.strptime(row['Posting Date'].strip(), '%m/%d/%Y').date()
                        description = row['Description'].strip().lower()
                        details = row['Details'].strip()
                        amount = Decimal(row['Amount'].strip())
                        transaction_type = row['Type'].strip()
                        balance = Decimal(row['Balance'].strip())
                        check_or_slip = row.get('Check or Slip #', '').strip()
                        
                        with db_transaction.atomic():
                            transaction_obj, created = Transaction.objects.get_or_create(
                                details=details,
                                posting_date=posting_date,
                                description=description,
                                amount=amount,
                                transaction_type=transaction_type,
                                balance=balance,
                                check_or_slip=check_or_slip,
                            )
                            if created:
                                transactions_added += 1
                    except IntegrityError as e:
                        errors += 1
                        logger.error(f"Skipping duplicate or invalid data for transaction on {row['Posting Date']} with description {row['Description']}. Error: {str(e)}")
                    except Exception as e:
                        errors += 1
                        logger.error(f"Error processing row: {row}. Error: {str(e)}")
        finally:
            default_storage.delete(file_path)
            return JsonResponse({'message': 'File Uploaded and processed successfully', 'transactions_added': transactions_added, 'errors': errors}, status=200)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)