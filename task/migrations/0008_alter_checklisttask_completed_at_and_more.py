# Generated by Django 4.2.7 on 2023-11-02 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_usertoproject'),
        ('task', '0007_rename_user_task_director'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklisttask',
            name='completed_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='subtaskchecklist',
            name='completed_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Крайний срок'),
        ),
        migrations.AlterField(
            model_name='task',
            name='section_project',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.sectionproject', verbose_name='Этап в проекте'),
        ),
    ]
