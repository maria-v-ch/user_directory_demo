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
    user1 = User.objects.create_user(username='testuser1', password='12345')
    user2 = User.objects.create_user(username='testuser2', password='12345')
    admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin12345')
    
    client = APIClient()
    
    # Test user accessing their own profile
    client.force_authenticate(user=user1)
    response = client.get(reverse('api_user_detail', args=[user1.id]))
    assert response.status_code == 200
    assert response.data['username'] == 'testuser1'
    
    # Test user accessing another user's profile
    response = client.get(reverse('api_user_detail', args=[user2.id]))
    assert response.status_code == 403
    
    # Test admin accessing any user's profile
    client.force_authenticate(user=admin)
    response = client.get(reverse('api_user_detail', args=[user1.id]))
    assert response.status_code == 200
    assert response.data['username'] == 'testuser1'

@pytest.mark.django_db
def test_user_list_api():
    user = User.objects.create_user(username='testuser', password='12345')
    admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin12345')
    
    client = APIClient()
    
    # Test unauthenticated access
    response = client.get(reverse('api_user_list'))
    assert response.status_code == 401
    
    # Test authenticated user access
    client.force_authenticate(user=user)
    response = client.get(reverse('api_user_list'))
    assert response.status_code == 200
    
    # Test admin access
    client.force_authenticate(user=admin)
    response = client.get(reverse('api_user_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_update_api():
    user = User.objects.create_user(username='testuser', password='12345')
    other_user = User.objects.create_user(username='otheruser', password='12345')
    admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin12345')
    
    client = APIClient()
    
    # Test user updating their own profile
    client.force_authenticate(user=user)
    response = client.patch(reverse('api_user_update', args=[user.id]), {'first_name': 'Updated'})
    assert response.status_code == 200
    assert response.data['first_name'] == 'Updated'
    
    # Test user trying to update another user's profile
    response = client.patch(reverse('api_user_update', args=[other_user.id]), {'first_name': 'Unauthorized'})
    assert response.status_code == 403
    
    # Test admin updating any user's profile
    client.force_authenticate(user=admin)
    response = client.patch(reverse('api_user_update', args=[other_user.id]), {'first_name': 'Admin Updated'})
    assert response.status_code == 200
    assert response.data['first_name'] == 'Admin Updated'

# Add more API tests as needed
