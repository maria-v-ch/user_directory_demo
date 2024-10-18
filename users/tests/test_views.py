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
    assert 'testuser' in str(response.content)

@pytest.mark.django_db
def test_user_detail_view():
    user = User.objects.create_user(username='testuser', password='12345')
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('user_detail', args=[user.id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'testuser' in str(response.content)

@pytest.mark.django_db
def test_user_registration_view(client):
    url = reverse('register')
    response = client.post(url, {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newuserpass123',
        'password2': 'newuserpass123',
        'first_name': 'New',
        'last_name': 'User'
    })
    assert response.status_code in [200, 201, 302]  # Accept either OK, Created, or redirect
    assert User.objects.filter(username='newuser').exists()
