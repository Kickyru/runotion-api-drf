from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from project.models import UserToProject, Project
from service.error.error_view import TaskError, ChecklistError, SubtaskChecklistError
from service.filter.task import TaskFilter
from service.order_by.order_by import order_by
from service.pagination import Pagination
from service.task import get_new_code_task_by_project, get_new_position_checklist_by_user_to_task, \
    get_new_position_subtask_checklist_by_user_to_task
from service.validator import Validator
from task.models import Task, ChecklistTask, UserToTask, SubtaskChecklist
from task.serializers import TaskSerializer, DetailTaskSerializer, ChecklistTaskSerializer, SubtaskChecklistSerializer, \
    ChecklistTaskPreviewSerializer
# ============================
#   Получение всех задач
# ============================
from user.models import UserProfile


class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    error = TaskError()
    filter = TaskFilter

    @action(methods=['get'], detail=False)
    def get_tasks(self, request):
        filter_data = self.filter(request)
        user = filter_data.result.pop('user')

        user_tasks = self.queryset.filter(usertotask__user__user=user, **filter_data.result)
        director_tasks = Task.objects.filter(director__user=user, **filter_data.result)
        all_tasks = user_tasks.union(director_tasks).order_by(order_by(request))

        result = Pagination(request=request, queryset=all_tasks).get()
        result['results'] = self.serializer_class(result.get('results'), many=True).data
        return Response(result, status=status.HTTP_200_OK)

    # Создание задачи
    @action(methods=['post'], detail=False)
    def create_task(self, request):
        validator = Validator(request=request)
        if not validator.has_content(['name', 'project_id']):
            return self.error.is_not_content_form()
        name = request.data['name']
        project_id = request.data['project_id']

        current_user = UserProfile.objects.get(user=request.user)
        projects = Project.objects.filter(pk=project_id)
        if len(projects) == 0:
            return self.error.is_not_found()

        code = get_new_code_task_by_project(projects[0])
        task = Task.objects.create(name=name, code=code, director=current_user, project=projects[0])
        serializer = self.serializer_class(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ==============================
#   Детальная страница задачи
# ==============================-+
class DetailTaskView(viewsets.ModelViewSet):
    serializer_class = DetailTaskSerializer
    queryset = Task.objects.all()
    error = TaskError()
    permission_classes = [permissions.IsAuthenticated]

    # Получение данных о задаче
    @action(methods=['get'], detail=False)
    def get_detail_task(self, request, task_id):
        tasks = self.queryset.filter(pk=task_id)
        if len(tasks) == 0:
            self.error.is_not_found()

        task = tasks[0]
        user_to_project = UserToProject.objects.filter(user__user=request.user, project=task.project)
        if len(user_to_project) == 0:
            self.error.forbidden()

        result = self.serializer_class(task).data
        return Response(result, status=status.HTTP_200_OK)


# ==============================
#      Удаление таска
# ==============================
class TaskDeleteAPIView(DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()


# ==============================
#       Чеклист у задачи
# ==============================
class ChecklistTaskView(viewsets.ModelViewSet):
    serializer_class = ChecklistTaskSerializer
    queryset = ChecklistTask.objects.all()
    error = ChecklistError()
    permission_classes = [permissions.IsAuthenticated]

    # Получение всех чеклистов по задаче
    @action(methods=['get'], detail=False)
    def get_checklists(self, request, task_id):
        checklists = self.queryset.filter(user__task__id=task_id, user__user__user=request.user) \
            .order_by(order_by(request))
        if len(checklists) == 0:
            self.error.is_not_found()

        result = self.serializer_class(checklists, many=True).data
        return Response(result, status=status.HTTP_200_OK)

    # Создание чеклиста
    @action(methods=['post'], detail=False)
    def create_checklist(self, request, task_id):
        current_user = UserProfile.objects.get(user=request.user)
        tasks = Task.objects.filter(pk=task_id)
        if len(tasks) == 0:
            return self.error.is_not_found()

        user_to_tasks = UserToTask.objects.filter(user=current_user, task=tasks[0])
        if len(user_to_tasks) == 0:
            return self.error.is_not_found()

        new_position = get_new_position_checklist_by_user_to_task(user_to_tasks[0])
        name = request.data.get('name')
        if name is None:
            name = f'Чек-лист {new_position}'
        checklist = ChecklistTask.objects.create(user=user_to_tasks[0], name=name, position=new_position)
        serializer = self.serializer_class(checklist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#  Обновление данных у подзадачи чек-листа
class ChecklistUpdateAPIView(UpdateAPIView):
    queryset = ChecklistTask.objects.all()
    serializer_class = ChecklistTaskPreviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        new_position = serializer.validated_data.get('position')

        if new_position != instance.position:
            user_to_task = instance.user
            other_checklist = ChecklistTask.objects.filter(user=user_to_task, position__gte=new_position)

            for checklist in other_checklist:
                checklist.position += 1
                checklist.save()

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


#  Удаление чеклиста
class ChecklistTaskDeleteAPIView(DestroyAPIView):
    queryset = ChecklistTask.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()


# ==============================
#     Подзадачи у чеклистов
# ==============================
class SubtaskChecklistTaskView(viewsets.ModelViewSet):
    serializer_class = SubtaskChecklistSerializer
    queryset = SubtaskChecklist.objects.all()
    error = SubtaskChecklistError()
    permission_classes = [permissions.IsAuthenticated]

    # Получение всех чеклистов по задаче
    @action(methods=['get'], detail=False)
    def get_subtasks_checklist(self, request, checklist_id):
        subtasks = self.queryset.filter(checklist__id=checklist_id, checklist__user__user__user=request.user) \
            .order_by(order_by(request))
        if len(subtasks) == 0:
            self.error.is_not_found()

        result = self.serializer_class(subtasks, many=True).data
        return Response(result, status=status.HTTP_200_OK)

    # Создание подзадач у чеклистов
    @action(methods=['post'], detail=False)
    def create_subtask(self, request, checklist_id):
        current_user = UserProfile.objects.get(user=request.user)
        checklists = ChecklistTask.objects.filter(pk=checklist_id, user__user=current_user)
        if len(checklists) == 0:
            return self.error.is_not_found()

        new_position = get_new_position_subtask_checklist_by_user_to_task(checklists[0])
        name = request.data.get('name')
        if name is None:
            name = f'Подзадача {new_position}'
        subtask = SubtaskChecklist.objects.create(checklist=checklists[0], name=name, position=new_position)
        serializer = self.serializer_class(subtask)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#  Обновление данных у подзадачи чек-листа
class SubtaskChecklistUpdateAPIView(UpdateAPIView):
    queryset = SubtaskChecklist.objects.all()
    serializer_class = SubtaskChecklistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        new_position = serializer.validated_data.get('position')

        if new_position != instance.position:
            checklist = instance.checklist
            other_subtasks = SubtaskChecklist.objects.filter(checklist=checklist, position__gte=new_position)

            for subtask in other_subtasks:
                subtask.position += 1
                subtask.save()

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


#  Удаление подзадачи у чек-листа
class SubtaskChecklistTaskDeleteAPIView(DestroyAPIView):
    queryset = SubtaskChecklist.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()
