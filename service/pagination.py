from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.utils.urls import replace_query_param


class PaginationValue:
    """Значения пагинаций моделей"""
    LIMIT = 30
    PAGE_QUERY_PARAM = 'page'


class Pagination:
    """Пагинация моделей"""

    def __init__(self, request, queryset, data=None, limit=None):
        limit = self._get_limit(request, limit)
        self.paginator = Paginator(queryset, limit)
        self.request = request
        self.link = request.build_absolute_uri()
        self.current_page_num = self.get_current_page_num()
        self.page_obj = self.get_page()
        self.data = data

    @staticmethod
    def _get_limit(request=None, limit=None):
        if request is None:
            return PaginationValue.LIMIT
        local_limit = request.query_params.get('limit')
        if local_limit is None:
            if limit is None or limit < 1:
                return PaginationValue.LIMIT
            return limit
        return int(local_limit)

    def get(self):
        """Возвращает каркас к пагинации"""
        return {
            "count": self.get_count(),
            "pages": self.get_num_pages(),
            "next": self.get_link_next_page(),
            "previous": self.get_link_previous_page(),
            "current_page": self.current_page_num,
            "results": self.page_obj
        }

    def get_current_page_num(self):
        """Вернет текущий номер пагинации"""
        return int(self.request.GET.get('page', 1))

    def get_page(self):
        """Вернет страницу"""
        try:
            return self.paginator.page(self.current_page_num)
        except PageNotAnInteger:
            return self.paginator.page(1)
        except EmptyPage:
            return self.paginator.page(self.paginator.num_pages)
        except ZeroDivisionError:
            return {}

    def get_num_pages(self):
        """Вернет количество страниц"""
        try:
            return self.paginator.num_pages
        except ZeroDivisionError:
            return 0

    def get_count(self):
        """Количество записей"""
        return self.paginator.count

    def get_link_next_page(self):
        """Следующая страница"""
        if type(self.page_obj) == dict:
            return None

        if not self.page_obj.has_next():
            return None

        page_number = self.page_obj.next_page_number()
        return replace_query_param(self.link, PaginationValue.PAGE_QUERY_PARAM, page_number)

    def get_link_previous_page(self):
        """Предыдущая страница"""
        if type(self.page_obj) == dict:
            return None

        if not self.page_obj.has_previous():
            return None

        page_number = self.page_obj.previous_page_number()
        return replace_query_param(self.link, PaginationValue.PAGE_QUERY_PARAM, page_number)
