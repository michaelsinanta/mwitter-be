from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from .utils import get_tokens_for_user
from .models import MyUser
from .serializers import RegistrationSerializer, PasswordChangeSerializer, UserSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your views here.


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            serializer = UserSerializer(user)
            return Response({'msg': 'Login Success', 'data' : serializer.data, 'token' : auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

      
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)
      
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) #Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_201_CREATED)

class UserList(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        User = get_user_model()
        users = User.objects.exclude(id=request.user.id)  # exclude authenticated user by ID
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try : 
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        except :
            return Response({
                'error' : 'User does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request):
        try :
            serializer = UserSerializer(request.user, data = request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': "Update success",
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response({
                'error' : 'User does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        
class SearchUser(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^username']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(id=self.request.user.id)
        return queryset.filter(Q(username__icontains=self.request.GET.get('search')))

