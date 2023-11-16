from task.models import UserPositionTask


def get_responsible_task():
    return UserPositionTask.objects.get(name='Ответственный')


def get_collaborator_task():
    return UserPositionTask.objects.get(name='Соисполнитель')


def get_observer_task():
    return UserPositionTask.objects.get(name='Наблюдатель')
