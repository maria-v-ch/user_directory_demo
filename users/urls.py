from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Template URLs
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('users/update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    
    # API URLs
    path('api/register/', views.APIUserRegistrationView.as_view(), name='api_register'),
    path('api/login/', views.APIUserLoginView.as_view(), name='api_login'),
    path('api/users/', views.APIUserListView.as_view(), name='api_user_list'),
    path('api/users/<int:pk>/', views.APIUserDetailView.as_view(), name='api_user_detail'),
    path('api/users/update/<int:pk>/', views.APIUserUpdateView.as_view(), name='api_user_update'),
]
