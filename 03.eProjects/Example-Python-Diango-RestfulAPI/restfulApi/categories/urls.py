# myapp/urls.py
from rest_framework import routers
from django.urls import include, path
from .views import CategoryViewSet

router = routers.DefaultRouter()
router.register('', CategoryViewSet)

urlpatterns = [
    # ...
    path('categories/', include(router.urls)),
]
