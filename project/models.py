from django.db import models
from core.models import ImportanceLevel
from user.models import UserProfile


# ===============
#     Проект
# ==============
class Project(models.Model):
    admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Админ')
    name = models.CharField('Название', max_length=128)
    code = models.CharField('Код', max_length=128)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    image = models.ImageField('Изображение', upload_to='project/images/', null=True, default=None, blank=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name


# ===================
#   Роль в проекте
# ===================
class RoleProject(models.Model):
    name = models.CharField('Название', max_length=128)
    level = models.OneToOneField(ImportanceLevel, on_delete=models.CASCADE, verbose_name='Уровень')

    class Meta:
        verbose_name = "Роль в проекте"
        verbose_name_plural = "Роли в проекте"

    def __str__(self):
        return self.name


# ==============================
#     Пользователь к проекту
# =============================
class UserToProject(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    role = models.ForeignKey(RoleProject, on_delete=models.CASCADE, verbose_name='Роль')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Пользователь к проекту"
        verbose_name_plural = "Пользователь к проектам"

    def __str__(self):
        return f'{self.project} {self.user} {self.role}'


# ===============================
#   Этапы в проекте (Канбан)
# ===============================
class SectionProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    name = models.CharField('Название', max_length=128)
    position = models.CharField('Позиция', max_length=128)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "Этапы проекта"
        verbose_name_plural = "Этапы проектов"

    def __str__(self):
        return f"{self.project.name} ===> {self.name}"


# =========================
#   Активность в проекте
# =========================
class ActionProject(models.Model):
    name = models.CharField('Название', max_length=128)

    class Meta:
        verbose_name = "Активность проекта"
        verbose_name_plural = "Активности проектов"

    def __str__(self):
        return self.name


# ======================
#   История проекта
# ======================
class HistoryProject(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='history_projects_created')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    action = models.ForeignKey(ActionProject, on_delete=models.CASCADE, verbose_name='Активность')
    victim = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Жертва', related_name='history_projects_affected')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = "История проекта"
        verbose_name_plural = "История проекта"

    def __str__(self):
        return f"{self.project.name} ===> {self.user.name}"
