import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from skillzor.models import Employee


@pytest.mark.django_db
def test_employee_list_returns_200():
    Employee.objects.create(
        first_name="Test", last_name="User", department="IT", job_title="Dev"
    )
    user = User.objects.create_user(username="tester")
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/employees/")
    assert response.status_code == 200
