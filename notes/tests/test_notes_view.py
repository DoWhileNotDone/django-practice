import pytest
from django.contrib.auth.models import User
from notes.models import Notes
from factories import UserFactory

@pytest.fixture
def logged_user(client):
    user = UserFactory()
    client.login(username=user.username, password='password')
    return user

@pytest.mark.django_db
def test_list_endpoint_return_user_notes(client, logged_user):

    note = Notes.objects.create(title='title', note='text', user=logged_user)

    response = client.get(path='/notes')
    assert 200 == response.status_code
    content = str(response.content)

    assert note.title in content
    assert 1 == content.count('<h3>')

@pytest.mark.django_db
def test_create_endpoint(client, logged_user):
    form_data: dict = {'title': 'Django Title', 'note': 'Django Text'}

    response = client.post(path='/notes/create', data=form_data, follow=True)
    assert 200 == response.status_code
    assert 'notes/notes_list.html' in response.template_name
    assert 1 == logged_user.notes.count()
    assert 'Django Text'  == logged_user.notes.first().note