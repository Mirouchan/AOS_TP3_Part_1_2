from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group

User = get_user_model()

#register
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role', 'lecteur')

    user = User.objects.create_user(username=username, password=password)
    user.role = role
    user.save()

    group = Group.objects.get(name='Lecteur' if role == 'lecteur' else 'Bibliothecaire')
    user.groups.add(group)

    return Response({"message": "User created"})

#login
@api_view(['POST'])
def login(request):
    from django.contrib.auth import authenticate

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    })
