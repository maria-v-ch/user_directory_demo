from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, UserSerializer
from django.contrib.auth import get_user_model
from .permissions import IsAdminUser, IsOwnerOrAdmin, CanViewProfile
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import Http404
import random
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Create your views here.

User = get_user_model()

logger = logging.getLogger(__name__)

def add_color_seed(request):
    if 'color_seed' not in request.session:
        request.session['color_seed'] = random.randint(1, 1000000)

class BaseView:
    def dispatch(self, request, *args, **kwargs):
        add_color_seed(request)
        return super().dispatch(request, *args, **kwargs)

class HomePageView(BaseView, TemplateView):
    template_name = 'home.html'

class UserRegistrationView(BaseView, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')  # Redirect to login page after registration

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Log the user in after registration
        return response

class UserLoginView(BaseView, LoginView):
    template_name = 'users/login.html'
    authentication_form = UserLoginForm

class UserListView(BaseView, LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    authentication_classes = [SessionAuthentication, BasicAuthentication]

class UserDetailView(BaseView, LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not CanViewProfile().has_object_permission(self.request, self, obj):
            raise PermissionDenied
        return obj

class UserUpdateView(BaseView, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_update.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not IsOwnerOrAdmin().has_object_permission(self.request, self, obj):
            raise PermissionDenied
        return obj

@login_required
def user_profile(request):
    add_color_seed(request)
    return render(request, 'users/user_detail.html', {'user': request.user})

class AdminUserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow anyone to register

    @swagger_auto_schema(
        operation_description="List all users or create a new user",
        responses={200: UserSerializer(many=True), 201: UserSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserSerializer,
        responses={201: UserSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]

    @swagger_auto_schema(
        operation_description="Retrieve a user by ID",
        responses={200: UserSerializer(), 403: "Forbidden", 404: "Not Found"}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a user",
        responses={204: "No Content", 403: "Forbidden", 404: "Not Found"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

# Error handling views
def bad_request(request, exception=None):
    return render(request, 'errors/400.html', status=400)

def permission_denied(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def page_not_found(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def server_error(request):
    return render(request, 'errors/500.html', status=500)

class UserRegistrationView(APIView):
    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={201: UserSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"New user registered: {user.username}")
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        logger.warning(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(TokenObtainPairView):
    @swagger_auto_schema(
        request_body=CustomTokenObtainPairSerializer,
        responses={200: openapi.Response("Successful login", CustomTokenObtainPairSerializer)}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all users",
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CanViewProfile]

    @swagger_auto_schema(
        operation_description="Retrieve a user by ID",
        responses={200: UserSerializer(), 403: "Forbidden", 404: "Not Found"}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]

    @swagger_auto_schema(
        operation_description="Update a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

# Add similar decorators and logging to your other views
