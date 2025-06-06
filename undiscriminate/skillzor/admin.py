# Admin Registration
from django.contrib import admin
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

admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Budget)
admin.site.register(Skill)
admin.site.register(EmployeeSkill)
admin.site.register(Certification)
admin.site.register(EmployeeCertification)
admin.site.register(DevelopmentAction)
