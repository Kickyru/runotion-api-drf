class Validator:
    def __init__(self, request):
        self.request = request

    def has_content(self, need_data):
        keys = list(self.request.data.keys())
        lack = []
        for el in need_data:
            if el not in keys:
                lack.append(el)
        return not bool(lack)
