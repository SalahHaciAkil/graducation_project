from django.http import JsonResponse
class GlobalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before it reaches the endpoint
        # Access the request object here and perform any necessary operations
        print(request.path)
        response = self.get_response(request)

        # Code to be executed for each response
        # You can modify the response here if needed

        return response

    def process_exception(self, request, exception):
        # Handle the exception and return a custom JSON response
        error_message = str(exception)
        return JsonResponse({'error': error_message}, status=500)