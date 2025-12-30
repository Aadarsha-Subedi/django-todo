from django.urls import path

from . import views

urlpatterns = [
    path("create-task/", views.create_task, name="create_task"),
    path("get-task/", views.get_all_tasks, name="get_task"),
    path("delete-task/<int:todo_id>/", views.delete_task, name="delete-task"),
    path("update-task/<int:todo_id>/", views.update_task, name="update-task")
]