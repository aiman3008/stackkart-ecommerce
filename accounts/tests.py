import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_can_be_created():
    user = User.objects.create_user(username='ali', email='ali@example.com', password='StrongPass123')
    assert user.check_password('StrongPass123')
