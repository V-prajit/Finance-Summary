from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
# Create your views here.
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No File Uploaded'}, status = 400)
        file = request.FILES['file']
        if allowed_file(file.name):
            file_name = default_storage.save(file.name, file)
            return JsonResponse({'message': 'File Uploaded successfully', 'file_path': file_name}, status = 200)
        else:
            return JsonResponse({'error': 'File Extension Not Allowed'}, status = 400)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status = 405)

def hello_world(response):
    return HttpResponse("<h1>Hello World<h1>")