from django.contrib.auth import authenticate
from users.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserRegisterSerializer


# Create your views here.


class UserLoginApiView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            response = {
                'success': 'True',
                'token': token.key,
                'user': user.username,
                'created': created

            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class UserLogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': True,
                'user': serializer.data,
                'token': Token.objects.get(user=User.objects.get(username=serializer.data['username'])).key
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)
