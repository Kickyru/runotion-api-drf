from .error import ErrorHelper


class ProjectError(ErrorHelper):
    def is_exists(self):
        return self.get_error(error="Такой проект уже существует", status=self.BAD_REQUEST)

    def is_not_found(self):
        return self.get_error(error="Такого проекта не существует", status=self.NOT_FOUND)


class TaskError(ErrorHelper):
    def is_not_found(self):
        return self.get_error(error="Такой задачи не существует", status=self.NOT_FOUND)


class ChecklistError(ErrorHelper):
    def is_not_found(self):
        return self.get_error(error="Такого чеклиста не существует", status=self.NOT_FOUND)


class SubtaskChecklistError(ErrorHelper):
    def is_not_found(self):
        return self.get_error(error="Такой подзадачи у чеклиста не существует", status=self.NOT_FOUND)
