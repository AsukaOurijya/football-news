from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

    if request.content_type == 'application/json':
        try:
            payload = request.body.decode('utf-8') or '{}'
            data = json.loads(payload)
        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON payload."
            }, status=400)
        username = data.get('username', '')
        password = data.get('password', '')
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Login status successful.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login successful!"
                # Add other data if you want to send data to Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, account is disabled."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, please check your username or password."
        }, status=401)
    
@csrf_exempt
def register(request):
    print(request)
    if request.method != 'POST':
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

    data = {}
    if request.content_type == 'application/json':
        try:
            payload = request.body.decode('utf-8') or '{}'
            data = json.loads(payload)
        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON payload."
            }, status=400)
    else:
        data = request.POST

    username = data.get('username', '')
    password1 = data.get('password1', '')
    password2 = data.get('password2', '')

    # Check if the passwords match
    if password1 != password2:
        return JsonResponse({
            "status": False,
            "message": "Passwords do not match."
        }, status=400)
    
    # Check if the username is already taken
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "status": False,
            "message": "Username already exists."
        }, status=400)
    
    # Create the new user
    user = User.objects.create_user(username=username, password=password1)
    user.save()
    
    return JsonResponse({
        "username": user.username,
        "status": 'success',
        "message": "User created successfully!"
    }, status=200)
