"""
Viewsets for managing application models.
"""

from rest_framework import viewsets
from .models import (
    Employee,
    Project,
    Budget,
    Skill,
    EmployeeSkill,
    Certification,
    EmployeeCertification,
    DevelopmentAction,
)
from .serializers import (
    EmployeeSerializer,
    ProjectSerializer,
    BudgetSerializer,
    SkillSerializer,
    EmployeeSkillSerializer,
    CertificationSerializer,
    EmployeeCertificationSerializer,
    DevelopmentActionSerializer,
)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class EmployeeSkillViewSet(viewsets.ModelViewSet):
    queryset = EmployeeSkill.objects.all()
    serializer_class = EmployeeSkillSerializer


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


class EmployeeCertificationViewSet(viewsets.ModelViewSet):
    queryset = EmployeeCertification.objects.all()
    serializer_class = EmployeeCertificationSerializer


class DevelopmentActionViewSet(viewsets.ModelViewSet):
    queryset = DevelopmentAction.objects.all()
    serializer_class = DevelopmentActionSerializer
