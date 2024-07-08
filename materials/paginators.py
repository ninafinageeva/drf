from rest_framework.pagination import PageNumberPagination


class CoursePaginator(PageNumberPagination):
    """ Пагинация для вывода курсов. """
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100


class LessonPaginator(PageNumberPagination):
    """ Пагинация для вывода уроков. """
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100
