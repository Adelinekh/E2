import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import make_prediction
from .views import SearchHistory
import json
from datetime import datetime

@pytest.mark.django_db
def test_good_prediction():
    good_input = {
        'Age_house': '19',
        'Total_SF': '2700',
        'Gr_Liv_Area': '1800',
        'Garage_Area': '500',
        'Overall_Qual': '8',
        'Bath': '2',
        'Exter_Qual': 'TA',
        'Kitchen_Qual': 'Gd',
        'Neighborhood': 'CollgCr'
    }

    prediction = make_prediction(good_input)

    assert prediction == 216859


@pytest.mark.django_db
def test_wrong_prediction():
    wrong_input = {
        'Age_house': '19',
        'Total_SF': '2700',
        'Gr_Liv_Area': '1800',
        'Garage_Area': '500',
        'Overall_Qual': '8',
        'Bath': '2',
        'Exter_Qual': '24',  # Modified value to match the input
        'Kitchen_Qual': 'Gd',
        'Neighborhood': 'CollgCr'
    }

    prediction = make_prediction(wrong_input)
    assert prediction == 0


@pytest.mark.django_db
def test_index_view(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200






@pytest.mark.django_db
def test_predict_view_post_method_wrong_input(client):
    url = reverse('predict')
    data = {
        'Year_Built': '1990',
        'Total_Bsmt_SF': '1000',
        'Flr_SF': '1200',
        'Gr_Liv_Area': '1800',
        'Garage_Area': '500',
        'Overall_Qual': '8',
        'Bath': '2',
        'Exter_Qual': '24',  # Modified value to match the input
        'Kitchen_Qual': 'Gd',
        'Neighborhood': 'CollgCr'
    }

    # Create and log in a user
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_login(user)

    response = client.post(url, data)
    assert response.status_code == 200
    assert response.content == b"The Input is not Correct"


@pytest.mark.django_db
def test_predict_view_get_method(client):
    url = reverse('predict')
    response = client.get(url)
    
    # Vérifie que le type de contenu est HTML
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/html; charset=utf-8'


@pytest.mark.django_db
def test_register_view(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    


@pytest.mark.django_db
def test_search_history_view_authenticated_user(client):
    url = reverse('search_history')
    # Create and log in a user
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_search_history_view_unauthenticated_user(client):
    url = reverse('search_history')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login')

@pytest.mark.django_db
def test_clear_search_view_existing_search(client):
    # Create and log in a user
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_login(user)

    # Create a search history entry
    search = SearchHistory.objects.create(user=user, input_variables={}, prediction_result=0)

    url = reverse('clear_search', args=[search.id])
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('search_history')
    assert not SearchHistory.objects.filter(id=search.id).exists()

@pytest.mark.django_db
def test_clear_search_view_nonexistent_search(client):
    # Create and log in a user
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_login(user)

    non_existent_search_id = 999
    url = reverse('clear_search', args=[non_existent_search_id])
    response = client.post(url)
    assert response.status_code == 404
    assert SearchHistory.objects.filter(id=non_existent_search_id).exists()




@pytest.mark.django_db
def test_search_history_view_unauthenticated_user(client):
    url = reverse('search_history')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + url  # Modify the assertion to include '?next='


@pytest.mark.django_db
def test_clear_search_view_nonexistent_search(client):
    # Create and log in a user
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_login(user)

    non_existent_search_id = 999
    url = reverse('clear_search', args=[non_existent_search_id])
    response = client.post(url)
    assert response.status_code == 404
    assert not SearchHistory.objects.filter(id=non_existent_search_id).exists()  # Modify the assertion to check if the search doesn't exist




import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_predict_view_post_method_good_input(client):
    # Créer un utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpass')

    # Connecter l'utilisateur
    client.force_login(user)

    url = reverse('predict')
    data = {
        'Year_Built': '2000',
        'Total_Bsmt_SF': '1500',
        'Flr_SF': '2000',
        'Gr_Liv_Area': '2500',
        'Garage_Area': '500',
        'Overall_Qual': '7',
        'Bath': '2',
        'Exter_Qual': 'Gd',
        'Kitchen_Qual': 'TA',
        'Neighborhood': 'CollgCr'
    }
    response = client.post(url, data)
    
  
    assert response.status_code == 200

@pytest.mark.django_db
def test_register_view_post_method(client):
    url = reverse('register')
    data = {
        'username': 'testuser',
        'password1': 'testpass',
        'password2': 'testpass'
    }
    response = client.post(url, data)
    
    # Vérifie si la redirection a eu lieu
    assert response.status_code == 200 # Vérifie que le code de statut est 302 (redirection)
  
