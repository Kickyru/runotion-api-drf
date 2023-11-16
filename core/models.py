from django.db import models


# ==========================
#     Уровень важности
# ==========================
class ImportanceLevel(models.Model):
    name = models.CharField('Название', max_length=128)
    value = models.IntegerField('Степень важности')

    class Meta:
        verbose_name = "Уровень важности"
        verbose_name_plural = "Уровни важности"

    def __str__(self):
        return self.name
