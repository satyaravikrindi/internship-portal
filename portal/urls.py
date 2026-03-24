from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.Registration.as_view()),
    path('login/',views.Login.as_view()),

    path('dashboard/',views.Dashboard.as_view()),
    path('admin/create-task/', views.CreateTask.as_view()),

    path('intern/tasks/<int:task_id>/complete/', views.CompleteTask.as_view())
]