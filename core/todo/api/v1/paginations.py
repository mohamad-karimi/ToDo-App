from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    '''
    Create a custom pagination class to control the number of objects
    returned per page and customize the pagination response.
    '''
        
    page_size = 2

    def get_paginated_response(self, data):
        '''
        Return a customized paginated response containing navigation links,
        total objects, total pages, and the current page results.
        '''
                
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_obj': self.page.paginator.count,
            'total_page': self.page.paginator.num_pages,
            'results': data
        })