"""
URL routing for application viewsets.
"""

from rest_framework.routers import DefaultRouter
from .views import (
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
router.register(r"employees", EmployeeViewSet)
router.register(r"projects", ProjectViewSet)
router.register(r"budgets", BudgetViewSet)
router.register(r"skills", SkillViewSet)
router.register(r"employee-skills", EmployeeSkillViewSet)
router.register(r"certifications", CertificationViewSet)
router.register(r"employee-certifications", EmployeeCertificationViewSet)
router.register(r"development-actions", DevelopmentActionViewSet)

urlpatterns = router.urls
