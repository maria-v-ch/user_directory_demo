import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import Client

User = get_user_model()

@pytest.mark.django_db
def test_user_list_view():
    user = User.objects.create_user(username='testuser', password='12345')
    client = Client()
    client.login(username='testuser', password='12345')
    url = reverse('user_list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_detail_view():
    user = User.objects.create_user(username='testuser', password='12345')
    client = Client()
    client.login(username='testuser', password='12345')
    url = reverse('user_detail', args=[user.id])
    response = client.get(url)
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
