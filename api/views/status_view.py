from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def status(request):
    """
    #### Check API Running Status 

    This endpoint allows clients to check the current status of the API. It is commonly 
    used for monitoring and ensuring that the API is operational. Upon a successful 
    GET request, it returns a `200` status code indicating that the API is up and running.
    """
    
    return Response({'status': 200}, status=200)
