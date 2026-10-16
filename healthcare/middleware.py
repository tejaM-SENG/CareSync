from django.shortcuts import redirect, render
from django.contrib import messages


class FirstLoginPasswordChangeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated and not request.user.is_staff:

            try:
                doctor = request.user.doctor_profile
            except Exception:
                doctor = None

            if (
                doctor
                and doctor.must_change_password
            ):
                allowed_paths = [
                    '/accounts/change-password/',
                    '/accounts/logout/',
                    '/admin/',
                    '/static/',
                    '/media/',
                ]

                if not any(
                    request.path.startswith(path)
                    for path in allowed_paths
                ):
                    return redirect('first_login_password_change')

        return self.get_response(request)



class Custom404Middleware:
    """
    Displays a custom 404 page whenever a request returns
    an HTTP 404 Not Found response.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return render(
                request,
                "healthcare/404.html",
                status=404
            )

        return response
