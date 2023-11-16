from service.filter.filter import Filter


class TaskFilter(Filter):
    COMPLETED = 'completed'

    def full(self):
        super().full()
        self.completed()

    def completed(self):
        if self.COMPLETED not in self.request.data.keys():
            return None
        self.result['completed_at__isnull'] = not self.request.data[self.COMPLETED]
