import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from undiscriminate.skillzor.models import Employee, Skill

@pytest.mark.django_db
def test_create_employee():
    client = APIClient()
    response = client.post(
        reverse("employee-list"),
        {
            "name": "Max Mustermann",
            "department": "Engineering",
            "job_title": "Developer",
        },
        format="json",
    )
    assert response.status_code == 201
    assert Employee.objects.count() == 1


@pytest.mark.django_db
def test_skill_creation():
    skill = Skill.objects.create(
        name="Python", description="Python programming language"
    )
    assert skill.name == "Python"
