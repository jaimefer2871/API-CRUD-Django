from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskView

routerTask = DefaultRouter()

routerTask.register(r'tasks', TaskView)
urlpatterns = [
    path("v1/", include(routerTask.urls)),
]
