import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_registration_api():
    client = APIClient()
    url = reverse('api_register')
    data = {
        'username': 'testuser',
        'password': 'testpass123',
        'password2': 'testpass123',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.get().username == 'testuser'

@pytest.mark.django_db
def test_user_login_api():
    User.objects.create_user(username='testuser', password='testpass123')
    client = APIClient()
    url = reverse('api_login')
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_user_detail_api():
    user = User.objects.create_user(username='testuser', password='12345')
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('api_user_detail', args=[user.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['username'] == 'testuser'

# Add more API tests as needed
