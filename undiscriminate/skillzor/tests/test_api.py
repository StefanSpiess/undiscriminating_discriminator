import pytest
from django.contrib.auth.models import Permission, User
from rest_framework.test import APIClient

from skillzor.models import Employee, EmployeeSkill, Skill


def client_with_perms(*codenames):
    user = User.objects.create_user(username="u-" + "-".join(codenames or ("none",)))
    user.user_permissions.set(Permission.objects.filter(codename__in=codenames))
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def employee(db):
    return Employee.objects.create(
        first_name="Test", last_name="User", department="IT", job_title="Dev"
    )


# --- CRUD permissions -------------------------------------------------------


@pytest.mark.django_db
def test_anonymous_requests_are_rejected(employee):
    response = APIClient().get("/api/employees/")
    assert response.status_code in (401, 403)  # nosec B101


@pytest.mark.django_db
def test_logged_in_without_view_permission_cannot_read(employee):
    response = client_with_perms().get("/api/employees/")
    assert response.status_code == 403  # nosec B101


@pytest.mark.django_db
def test_view_permission_allows_read_but_not_write(employee):
    client = client_with_perms("view_employee")
    assert client.get("/api/employees/").status_code == 200  # nosec B101
    response = client.post(
        "/api/employees/",
        {"first_name": "A", "last_name": "B", "department": "X", "job_title": "Y"},
        format="json",
    )
    assert response.status_code == 403  # nosec B101


@pytest.mark.django_db
def test_add_permission_allows_create():
    client = client_with_perms("view_employee", "add_employee")
    response = client.post(
        "/api/employees/",
        {"first_name": "A", "last_name": "B", "department": "X", "job_title": "Y"},
        format="json",
    )
    assert response.status_code == 201  # nosec B101


# --- validation -------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("level,expected", [(0, 400), (1, 201), (5, 201), (6, 400)])
def test_proficiency_level_follows_ecf_scale(employee, level, expected):
    skill = Skill.objects.create(name="Python", description="")
    client = client_with_perms("add_employeeskill")
    response = client.post(
        "/api/employee-skills/",
        {"employee": employee.id, "skill": skill.id, "proficiency_level": level},
        format="json",
    )
    assert response.status_code == expected, response.content  # nosec B101


# --- AI export endpoint -----------------------------------------------------


@pytest.fixture
def five_devs(db):
    skill = Skill.objects.create(
        name="Python", description="", framework_ref="e-CF:B.1"
    )
    for i in range(5):
        e = Employee.objects.create(
            first_name=f"Dev{i}", last_name="Secret", department="Eng", job_title="Dev"
        )
        EmployeeSkill.objects.create(employee=e, skill=skill, proficiency_level=3)


@pytest.mark.django_db
def test_export_requires_dedicated_permission(five_devs):
    # Even full read access to employees does not grant the export.
    client = client_with_perms("view_employee", "view_employeeskill")
    assert client.get("/api/ai-export/").status_code == 403  # nosec B101


@pytest.mark.django_db
def test_export_returns_pseudonymised_records(five_devs):
    client = client_with_perms("export_pseudonymized_profiles")
    response = client.get("/api/ai-export/")
    assert response.status_code == 200  # nosec B101
    body = response.json()
    assert len(body["records"]) == 5  # nosec B101
    assert "Secret" not in response.content.decode()  # nosec B101
    assert body["records"][0]["department"] == "Eng"  # nosec B101


@pytest.mark.django_db
@pytest.mark.parametrize(
    "k,expected", [("4", 400), ("abc", 400), ("5", 200), ("6", 200)]
)
def test_export_k_can_only_be_raised(five_devs, settings, k, expected):
    settings.EXPORT_MIN_K = 5
    client = client_with_perms("export_pseudonymized_profiles")
    response = client.get(f"/api/ai-export/?k={k}")
    assert response.status_code == expected  # nosec B101
    if k == "6":
        assert response.json()["privacy"]["withheld"] is True  # nosec B101
