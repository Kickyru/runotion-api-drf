from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# =============================
#   Расширенные пользователи
# =============================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user/images/')

    class Meta:
        verbose_name = "Расширенный пользователь"
        verbose_name_plural = "Расширенные пользователи"

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()