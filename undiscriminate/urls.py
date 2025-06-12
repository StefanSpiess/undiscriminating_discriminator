from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import your viewsets here
# from skillzor.views import YourViewSet

router = DefaultRouter()
# Register your viewsets here
# router.register(r'your_endpoint', YourViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),  # Ensure this is included
    ]
