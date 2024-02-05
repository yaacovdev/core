from django.http import JsonResponse


class ErrorMiddleware:
    """
    Middleware class for handling errors in the messaging system.

    Args:
        get_response: The callable that takes a request and returns a response.

    Attributes:
        get_response: The callable that takes a request and returns a response.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the incoming request and return the response.

        Args:
            request: The incoming request object.

        Returns:
            The response object.
        """
        response = self.get_response(request)
        if response.status_code in [400, 404, 500]:
            return self.create_json_error_response(response)
        return response

    def create_json_error_response(self, response):
        error_message = None
        error_details = None

        if response.status_code == 400:
            error_message = "Invalid data"
            try:
                error_details = self.get_error_details(response)
            except Exception as e:
                error_details = str(e)
        else:
            error_message = response.reason_phrase

        return JsonResponse(
            {
                "status": response.status_code,
                "error": error_message,
                "details": error_details,
            },
            status=response.status_code,
        )

    def get_error_details(self, response):
        """
        Retrieves the error details from the response.

        Args:
            response: The response object.

        Returns:
            The error details from the response, or "Error validating data." if the response does not have any data.
        """
        try:
            return response.data
        except AttributeError:
            return "Error validating data."
