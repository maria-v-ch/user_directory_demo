import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
def test_user_list_view():
    user = User.objects.create_user(username='testuser', password='12345')
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('user_list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_detail_view():
    user = User.objects.create_user(username='testuser', password='12345')
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('user_detail', args=[user.id])
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_registration_view(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    
    data = {
        'username': 'testuser',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'email': 'test@example.com'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after successful registration
    assert User.objects.count() == 1
    assert User.objects.get().username == 'testuser'

# Add more view tests as needed
