from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['is_staff'] = user.is_staff
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    
    if user is not None:
        tokens = get_tokens_for_user(user)
        return Response(tokens)
    else:
        return Response({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    return JsonResponse({'success': True})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username:
        return Response({'error': 'Username is required'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'error': 'Username already exists'}, status=400)
    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        tokens = get_tokens_for_user(user)
        return Response({
            'success': True,
            **tokens
        })
    except ValueError as e:
        return Response({'error': str(e)}, status=400)