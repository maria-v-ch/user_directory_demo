import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()

@pytest.mark.django_db
def test_user_list_view():
    # Create a regular user and an admin user
    user = User.objects.create_user(username='testuser', password='12345')
    admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin12345')
    
    client = Client()
    
    # Test regular user access
    client.login(username='testuser', password='12345')
    response = client.get(reverse('user_list'))
    assert response.status_code == 200
    assert 'users' in response.context
    assert all(isinstance(u, dict) for u in response.context['users'])
    
    # Test admin user access
    client.login(username='admin', password='admin12345')
    response = client.get(reverse('user_list'))
    assert response.status_code == 200
    assert 'users' in response.context
    assert all(isinstance(u, User) for u in response.context['users'])

@pytest.mark.django_db
def test_user_detail_view():
    user1 = User.objects.create_user(username='testuser1', password='12345')
    user2 = User.objects.create_user(username='testuser2', password='12345')
    admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin12345')
    
    client = Client()
    
    # Test user accessing their own profile
    client.login(username='testuser1', password='12345')
    response = client.get(reverse('user_detail', args=[user1.id]))
    assert response.status_code == 200
    
    # Test user accessing another user's profile
    response = client.get(reverse('user_detail', args=[user2.id]))
    assert response.status_code == 403
    
    # Test admin accessing any user's profile
    client.login(username='admin', password='admin12345')
    response = client.get(reverse('user_detail', args=[user1.id]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_registration_view(client):
    url = reverse('register')
    data = {
        'username': 'testuser',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after successful registration
    assert User.objects.count() == 1
    assert User.objects.get().username == 'testuser'

@pytest.mark.django_db
def test_user_login_view(client):
    User.objects.create_user(username='testuser', password='testpass123')
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after successful login

# Add more view tests as needed

@pytest.mark.django_db
def test_user_update_view():
    user = User.objects.create_user(username='testuser', password='12345')
    other_user = User.objects.create_user(username='otheruser', password='12345')
    admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin12345')
    
    client = Client()
    
    # Test user updating their own profile
    client.login(username='testuser', password='12345')
    response = client.get(reverse('user_update', args=[user.id]))
    assert response.status_code == 200
    
    # Test user trying to update another user's profile
    response = client.get(reverse('user_update', args=[other_user.id]))
    assert response.status_code == 403
    
    # Test admin updating any user's profile
    client.login(username='admin', password='admin12345')
    response = client.get(reverse('user_update', args=[user.id]))
    assert response.status_code == 200
