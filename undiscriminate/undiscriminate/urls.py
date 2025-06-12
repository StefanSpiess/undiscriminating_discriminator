"""
URL routing for application viewsets.
"""

from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path
from skillzor.views import (
    EmployeeViewSet,
    ProjectViewSet,
    BudgetViewSet,
    SkillViewSet,
    EmployeeSkillViewSet,
    CertificationViewSet,
    EmployeeCertificationViewSet,
    DevelopmentActionViewSet,
)

router = DefaultRouter()

router.register(
    prefix="employees",
    viewset=EmployeeViewSet,
    basename="employees",
)
router.register(
    prefix="projects",
    viewset=ProjectViewSet,
    basename="projects",
)
router.register(
    prefix="budgets",
    viewset=BudgetViewSet,
    basename="budgets",
)
router.register(
    prefix="skills",
    viewset=SkillViewSet,
    basename="skills",
)
router.register(
    prefix="employee-skills",
    viewset=EmployeeSkillViewSet,
    basename="employee-skills",
)
router.register(
    prefix="certifications",
    viewset=CertificationViewSet,
    basename="certifications",
)
router.register(
    prefix="employee-certifications",
    viewset=EmployeeCertificationViewSet,
    basename="employee-certifications",
)
router.register(
    prefix="development-actions",
    viewset=DevelopmentActionViewSet,
    basename="development-actions",
)

urlpatterns = [
    path("admin/", admin.site.urls),  # Add this line for the admin interface
] + router.urls
