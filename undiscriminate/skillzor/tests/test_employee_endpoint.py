import pytest
from rest_framework.test import APIClient
from skillzor.models import Employee


@pytest.mark.django_db
def test_employee_list_returns_200():
    Employee.objects.create(
        first_name="Test", last_name="User", department="IT", job_title="Dev"
    )
    client = APIClient()
    response = client.get("/employees/")
    assert response.status_code == 200
