from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework import generics, permissions
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

# Create your views here.

User = get_user_model()

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
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('user_list')

class UserLoginView(BaseView, LoginView):
    template_name = 'users/login.html'
    authentication_form = UserLoginForm

class UserListView(BaseView, LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserDetailView(BaseView, LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

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
    permission_classes = [IsAdminUser]

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# Error handling views
def bad_request(request, exception=None):
    return render(request, 'errors/400.html', status=400)

def permission_denied(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def page_not_found(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def server_error(request):
    return render(request, 'errors/500.html', status=500)
