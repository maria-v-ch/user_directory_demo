from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
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
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

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
        logger.info(f"New user registered and logged in: {self.object.username}")
        return response

class UserLoginView(BaseView, LoginView):
    template_name = 'users/login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        logger.info(f"User logged in: {form.get_user().username}")
        return super().form_valid(form)

class UserListView(BaseView, LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        logger.debug(f"User {self.request.user.username} accessed user list")
        return super().get_queryset()

class UserDetailView(BaseView, LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not CanViewProfile().has_object_permission(self.request, self, obj):
            logger.warning(f"User {self.request.user.username} attempted to access unauthorized profile: {obj.username}")
            raise PermissionDenied
        logger.info(f"User {self.request.user.username} viewed profile of {obj.username}")
        return obj

class UserUpdateView(BaseView, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_update.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not IsOwnerOrAdmin().has_object_permission(self.request, self, obj):
            logger.warning(f"User {self.request.user.username} attempted to update unauthorized profile: {obj.username}")
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"User {self.object.username} updated their profile")
        return response

@login_required
def user_profile(request):
    add_color_seed(request)
    logger.debug(f"User {request.user.username} accessed their profile")
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
        logger.info(f"Admin user list accessed by {request.user.username}")
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserSerializer,
        responses={201: UserSerializer()}
    )
    def post(self, request, *args, **kwargs):
        logger.info(f"New user creation attempted by {request.user.username}")
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
        logger.info(f"User detail accessed for user ID {kwargs.get('pk')} by {request.user.username}")
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
    )
    def put(self, request, *args, **kwargs):
        logger.info(f"User update attempted for user ID {kwargs.get('pk')} by {request.user.username}")
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
    )
    def patch(self, request, *args, **kwargs):
        logger.info(f"Partial user update attempted for user ID {kwargs.get('pk')} by {request.user.username}")
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a user",
        responses={204: "No Content", 403: "Forbidden", 404: "Not Found"}
    )
    def delete(self, request, *args, **kwargs):
        logger.warning(f"User deletion attempted for user ID {kwargs.get('pk')} by {request.user.username}")
        return super().delete(request, *args, **kwargs)

# Error handling views
def bad_request(request, exception=None):
    logger.error(f"400 Bad Request: {request.path}")
    return render(request, 'errors/400.html', status=400)

def permission_denied(request, exception=None):
    logger.error(f"403 Permission Denied: {request.path}")
    return render(request, 'errors/403.html', status=403)

def page_not_found(request, exception=None):
    logger.error(f"404 Page Not Found: {request.path}")
    return render(request, 'errors/404.html', status=404)

def server_error(request):
    logger.critical(f"500 Server Error: {request.path}")
    return render(request, 'errors/500.html', status=500)

class UserRegistrationView(APIView):
    throttle_classes = [AnonRateThrottle]
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
    throttle_classes = [AnonRateThrottle]
    @swagger_auto_schema(
        request_body=CustomTokenObtainPairSerializer,
        responses={200: openapi.Response("Successful login", CustomTokenObtainPairSerializer)}
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info(f"User logged in: {request.data.get('username')}")
        else:
            logger.warning(f"Failed login attempt for user: {request.data.get('username')}")
        return response

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @swagger_auto_schema(
        operation_description="List all users",
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        logger.info(f"User list accessed by {request.user.username}")
        return super().get(request, *args, **kwargs)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CanViewProfile]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @swagger_auto_schema(
        operation_description="Retrieve a user by ID",
        responses={200: UserSerializer(), 403: "Forbidden", 404: "Not Found"}
    )
    def get(self, request, *args, **kwargs):
        logger.info(f"User detail accessed for user ID {kwargs.get('pk')} by {request.user.username}")
        return super().get(request, *args, **kwargs)

class UserUpdateView(generics.UpdateAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]

    @swagger_auto_schema(
        operation_description="Update a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
    )
    def put(self, request, *args, **kwargs):
        logger.info(f"User update attempted for user ID {kwargs.get('pk')} by {request.user.username}")
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
    )
    def patch(self, request, *args, **kwargs):
        logger.info(f"Partial user update attempted for user ID {kwargs.get('pk')} by {request.user.username}")
        return super().patch(request, *args, **kwargs)

# Add similar decorators and logging to your other views
