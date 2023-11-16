from django.db import models

from core.models import ImportanceLevel
from project.models import Project, SectionProject
from user.models import UserProfile


# ===============
#     Задачи
# ==============
class Task(models.Model):
    director = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Постановщик')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    name = models.CharField('Название', max_length=128)
    code = models.CharField('Код', max_length=128)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    deadline = models.DateTimeField('Крайний срок', null=True, default=None, blank=True)
    completed_at = models.DateTimeField('Дата завершения', null=True, default=None, blank=True)
    section_project = models.ForeignKey(SectionProject, on_delete=models.SET_NULL, verbose_name='Этап в проекте',
                                        null=True, blank=True, default=None)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Task, self).save(*args, **kwargs)
        if created:
            responsible_task = UserPositionTask.objects.get(name='Ответственный')
            UserToTask.objects.create(user=self.director, task=self, position=responsible_task)


# ==========================================
#     Должность пользователя в задачах
# ==========================================
class UserPositionTask(models.Model):
    name = models.CharField('Название', max_length=128)
    level = models.ForeignKey(ImportanceLevel, on_delete=models.CASCADE, verbose_name='Уровень')

    class Meta:
        verbose_name = "Должность пользователя в задачах"
        verbose_name_plural = "Должности пользователя в задачах"

    def __str__(self):
        return self.name


# =============================
#     Пользователь к задаче
# =============================
class UserToTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    position = models.ForeignKey(UserPositionTask, on_delete=models.CASCADE,
                                 verbose_name='Должность пользователя в задачах')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Пользователь к задаче"
        verbose_name_plural = "Пользователи к задаче"

    def __str__(self):
        return f"{self.task.name} ===> {self.user.name}"


# =============================
#     Комментарии у задачи
# =============================
class CommentTask(models.Model):
    user = models.ForeignKey(UserToTask, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий у задачи"
        verbose_name_plural = "Комментарии у задачи"

    def __str__(self):
        return f"{self.task.name} ===> {self.user.name}"


# =============================
#     Чеклист у задачи
# =============================
class ChecklistTask(models.Model):
    user = models.ForeignKey(UserToTask, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField('Название', max_length=128)
    position = models.IntegerField('Позиция')
    completed_at = models.DateTimeField('Дата завершения', null=True, default=None, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Чеклист у задачи"
        verbose_name_plural = "Чеклисты у задачи"

    def __str__(self):
        return f"{self.user.task.name} ===> {self.name}"


# =============================
#     Подзадачи у чеклиста
# =============================
class SubtaskChecklist(models.Model):
    checklist = models.ForeignKey(ChecklistTask, on_delete=models.CASCADE, verbose_name='Чеклист')
    name = models.CharField('Название', max_length=128)
    position = models.IntegerField('Позиция')
    completed_at = models.DateTimeField('Дата завершения', null=True, default=None, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Подзадача в чеклисте"
        verbose_name_plural = "Подзадачи в чеклистах"

    def __str__(self):
        return f"{self.checklist.user.task.name} ==> {self.checklist.name} ===> {self.name}"
