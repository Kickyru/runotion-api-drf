class Filter:
    MY = 'my'
    USER_ID = 'user_id'

    def __init__(self, request):
        self.result: dict = {}
        self.request = request
        self.full()

    def full(self):
        self.is_my_task()
        self.has_user_id()

    def is_my_task(self):
        # if self.MY not in self.request.data.keys():
        #     return None
        self.result['user'] = self.request.user

    def has_user_id(self):
        if self.USER_ID not in self.request.data.keys():
            return None
        self.result['user'] = self.request.data[self.USER_ID]
