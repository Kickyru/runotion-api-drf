# Generated by Django 4.2.7 on 2023-11-02 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_alter_checklisttask_completed_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='user',
            new_name='director',
        ),
    ]
