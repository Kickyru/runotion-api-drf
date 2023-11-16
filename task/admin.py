from django.contrib import admin

from task.models import Task, UserPositionTask, UserToTask, CommentTask, ChecklistTask, SubtaskChecklist

admin.site.register(Task)
admin.site.register(UserPositionTask)
admin.site.register(UserToTask)
admin.site.register(CommentTask)
admin.site.register(ChecklistTask)
admin.site.register(SubtaskChecklist)
