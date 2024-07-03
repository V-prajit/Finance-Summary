from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User

@csrf_exempt
@require_POST
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status = 400)

@csrf_exempt
@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})

@csrf_exempt
@require_POST
def register_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'error': 'Username already exists'}, status=400)
    user = User.objects.create_user(username=username, password=password, email=email)
    login(request, user)
    return JsonResponse({'success': True})