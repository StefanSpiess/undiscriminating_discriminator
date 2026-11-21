"""
Permission classes.

HR data is sensitive by default: being logged in is not enough to read it.
Every request, reads included, must be backed by the matching Django model
permission (view/add/change/delete).
"""

from rest_framework.permissions import BasePermission, DjangoModelPermissions


class StrictModelPermissions(DjangoModelPermissions):
    """DjangoModelPermissions that also requires ``view_*`` for safe methods."""

    perms_map = {
        **DjangoModelPermissions.perms_map,
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
    }


class CanExportPseudonymizedProfiles(BasePermission):
    """Gate for the AI export: a dedicated, explicitly granted permission."""

    required = "skillzor.export_pseudonymized_profiles"

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.has_perm(self.required))
