from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000
    ordering = 'timestamp'

    # def get_paginated_response(self, data):
    #     return Response(data)