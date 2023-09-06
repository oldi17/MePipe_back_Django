from rest_framework.views import exception_handler
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response

def paginate(
        objects,
        req,
        Serializer,
        modelName='data',
        itemsPerPage=10,
):
    data = []
    nextPage = 1
    previousPage = 1
    model = objects
    page = req.GET.get('page', 1)
    paginator = Paginator(model, itemsPerPage)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = Serializer(data,context={'req': req} ,many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()

    return Response({
        modelName: serializer.data , 
        'count': paginator.count, 
        'numpages' : paginator.num_pages, 
        'nextlink': req.path + '?page=' + str(nextPage), 
        'prevlink': req.path + '?page=' + str(previousPage)})