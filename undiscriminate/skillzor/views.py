"""
Viewsets for managing application models, plus the privacy-preserving AI export.
"""

from django.conf import settings
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import CanExportPseudonymizedProfiles
from .privacy import build_export
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


class AIExportView(APIView):
    """
    GET /api/ai-export/?k=<int>

    Pseudonymised, k-anonymised skill profiles for downstream AI systems.
    ``k`` may only be raised above the configured minimum, never lowered.
    """

    permission_classes = [CanExportPseudonymizedProfiles]

    def get(self, request):
        min_k = settings.EXPORT_MIN_K
        raw_k = request.query_params.get("k", min_k)
        try:
            k = int(raw_k)
        except (TypeError, ValueError):
            raise ValidationError({"k": "Must be an integer."})
        if k < min_k:
            raise ValidationError({"k": f"Must be at least {min_k}."})
        return Response(build_export(k=k))
