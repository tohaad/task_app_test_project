from django.urls import path, include
from rest_framework import routers
from tasks.views import TaskGenericViewSet


router = routers.DefaultRouter()
router.register('tasks', TaskGenericViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
]
