from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task.views import TaskView, DetailTaskView, ChecklistTaskView, ChecklistTaskDeleteAPIView, TaskDeleteAPIView, \
    SubtaskChecklistTaskView, SubtaskChecklistTaskDeleteAPIView, SubtaskChecklistUpdateAPIView, ChecklistUpdateAPIView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # Все задачи
    path("all/", TaskView.as_view({'get': 'get_tasks'})),
    path("create/", TaskView.as_view({'post': 'create_task'})),

    # Детальная страница задачи
    path("<int:task_id>/", DetailTaskView.as_view({'get': 'get_detail_task'})),
    path("<int:pk>/delete/", TaskDeleteAPIView.as_view()),

    # Чеклист у задачи
    path("<int:task_id>/checklist/", ChecklistTaskView.as_view({'get': 'get_checklists'})),
    path("<int:task_id>/checklist/create/", ChecklistTaskView.as_view({'post': 'create_checklist'})),
    path("checklist/<int:pk>/update/", ChecklistUpdateAPIView.as_view()),
    path("checklist/<int:pk>/delete/", ChecklistTaskDeleteAPIView.as_view()),

    # Подзадачи у чеклистов
    path("checklist/<int:checklist_id>/subtask/", SubtaskChecklistTaskView.as_view({'get': 'get_subtasks_checklist'})),
    path("checklist/<int:checklist_id>/subtask/create/", SubtaskChecklistTaskView.as_view({'post': 'create_subtask'})),
    path("subtask/<int:pk>/update/", SubtaskChecklistUpdateAPIView.as_view()),
    path("subtask/<int:pk>/delete/", SubtaskChecklistTaskDeleteAPIView.as_view()),

]
