import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_list_view(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('user_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'testuser' in str(response.content)

@pytest.mark.django_db
def test_user_detail_view(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
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
        'password1': 'newuserpass123',
        'password2': 'newuserpass123',
    })
    assert response.status_code == 302  # Redirect after successful registration
    assert User.objects.filter(username='newuser').exists()
