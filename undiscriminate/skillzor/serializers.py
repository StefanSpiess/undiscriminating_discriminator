"""
Serializers for application models.
"""

from rest_framework import serializers
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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class EmployeeSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSkill
        fields = "__all__"


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = "__all__"


class EmployeeCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCertification
        fields = "__all__"


class DevelopmentActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevelopmentAction
        fields = "__all__"
