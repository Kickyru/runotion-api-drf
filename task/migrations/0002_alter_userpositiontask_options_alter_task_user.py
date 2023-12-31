# Generated by Django 4.2.7 on 2023-11-02 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpositiontask',
            options={'verbose_name': 'Должность пользователя в задачах', 'verbose_name_plural': 'Должности пользователя в задачах'},
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='Пользователь'),
        ),
    ]
