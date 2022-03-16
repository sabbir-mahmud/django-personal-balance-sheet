# imports
from django.urls import path
from . import views

# urls
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add_task', views.add_task, name='add-task'),
    path('edit_task/<str:pk>/', views.edit_task, name='edit-task'),
    path('task_done/<str:pk>/', views.done_task, name='done-task'),
    path('delete_task/<str:pk>/', views.delete_task, name='delete-task'),
]
