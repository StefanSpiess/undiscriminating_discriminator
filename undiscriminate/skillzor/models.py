"""
Django Models for the Skill Management Application.

This module defines the database models for managing employees, their skills, certifications,
projects, budgets, and development actions. It provides a structured way to track employee
competencies, certifications, and professional development activities within an organization.
"""

from django.db import models
from django.utils.timezone import now


# Core Models
class Employee(models.Model):
    """
    Represents an employee in the organization.

    Attributes:
        id (int): Primary key for the employee.
        name (str): Full name of the employee.
        department (str): Department where the employee works.
        job_title (str): Job title of the employee.
    """

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    last_updated = models.DateTimeField(default=now)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Project(models.Model):
    """
    Represents a project within the organization.

    Attributes:
        name (str): Name of the project.
        description (str): Detailed description of the project.
        start_date (date): Start date of the project.
        end_date (date): End date of the project.
    """

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class Budget(models.Model):
    """
    Represents a budget allocation for a project or activity.

    Attributes:
        name (str): Name of the budget.
        amount (Decimal): Total allocated amount.
        start_date (date): Start date of the budget period.
        end_date (date): End date of the budget period.
        description (str): Additional details about the budget.
    """

    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


# Skill Models
class Skill(models.Model):
    """
    Represents a skill that employees can possess.

    Attributes:
        name (str): Name of the skill.
        description (str): Detailed description of the skill.
        category (str): Category or domain of the skill.
        framework_ref (str): Reference to an external framework or standard.
    """

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    framework_ref = models.CharField(max_length=200, blank=True)
    last_updated = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class EmployeeSkill(models.Model):
    """
    Represents the association between an employee and a skill.

    Attributes:
        employee (Employee): The employee possessing the skill.
        skill (Skill): The skill possessed by the employee.
        proficiency_level (int): Level of proficiency in the skill.
        last_updated (date): Date when the skill was last updated.
        evidence (str): Evidence or notes supporting the skill claim.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.IntegerField()
    last_updated = models.DateTimeField(default=now)

    class Meta:
        unique_together = ("employee", "skill")


# Certification Models
class Certification(models.Model):
    """
    Represents a professional certification.

    Attributes:
        name (str): Name of the certification.
        issuer (str): Organization issuing the certification.
        description (str): Detailed description of the certification.
        validity_period (str): Validity period of the certification.
        external_ref (URL): External reference or link to the certification.
    """

    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    description = models.TextField()
    validity_period = models.CharField(max_length=50, blank=True)
    external_ref = models.URLField(blank=True)
    last_updated = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class EmployeeCertification(models.Model):
    """
    Represents the association between an employee and a certification.

    Attributes:
        employee (Employee): The employee holding the certification.
        certification (Certification): The certification held by the employee.
        issue_date (date): Date when the certification was issued.
        expiration_date (date): Expiration date of the certification, if applicable.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(default=now)
    evidence = models.TextField(blank=True)


# Learning Models
class DevelopmentAction(models.Model):
    """
    Represents a professional development action for an employee.

    Attributes:
        employee (Employee): The employee undergoing the development action.
        type (str): Type of development action (e.g., course, training, mentoring).
        title (str): Title of the development action.
        description (str): Detailed description of the development action.
        date (date): Date of the development action.
        duration (str): Duration of the development action.
        skill (Skill): Skill associated with the development action, if any.
        certification (Certification): Certification associated with the development action, if any.
        project (Project): Project associated with the development action, if any.
        budget (Budget): Budget associated with the development action, if any.
    """

    TRAINING_TYPES = [
        ("course", "Course"),
        ("training", "Training"),
        ("mentoring", "Mentoring"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TRAINING_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    duration = models.CharField(max_length=50, blank=True)
    skill = models.ForeignKey(Skill, null=True, blank=True, on_delete=models.SET_NULL)
    certification = models.ForeignKey(
        Certification, null=True, blank=True, on_delete=models.SET_NULL
    )
    project = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.SET_NULL
    )
    budget = models.ForeignKey(Budget, null=True, blank=True, on_delete=models.SET_NULL)
    last_updated = models.DateTimeField(default=now)
