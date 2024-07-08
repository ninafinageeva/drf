from rest_framework import pagination


class CoursePaginator(pagination.PageNumberPagination):
    """ Пагинация для вывода курсов. """
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100


class LessonPaginator(pagination.PageNumberPagination):
    """ Пагинация для вывода уроков. """
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100
