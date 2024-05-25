from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from django import forms
from .models import Scanner
from django.contrib.auth.mixins import UserPassesTestMixin


class ScanView(UserPassesTestMixin, TemplateView):
    template_name = "scan/scan.html"

    def test_func(self):
        return self.request.session.get('scanner_id')

    def handle_no_permission(self):
        return redirect('scanner_login')


@ensure_csrf_cookie
def validate_qrcode(request):
    """
    the @ensure_csrf_cookie decorator is used to include the CSRF token in the response to the client.
    This is done by setting the csrftoken cookie in the client's browser.
    On the HTML side, the $.ajaxSetup() function is used to set the X-CSRFToken header of the Ajax requests to the value
    of the csrftoken cookie.
    The getCookie() function retrieves the value of the csrftoken cookie from the client's browser.
    The Ajax request is triggered when a qrcode is scanned.
    The $.ajax() function sends a POST request to this view with the scanned content in the data field.
    When the server responds, the success function displays a message with the response data.
    If there is an error, the error function displays a message with the error message.
    """
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':
        content = request.POST.get('content', '')
        # Process the scanned string here
        return JsonResponse({'status': 'success', 'message': 'Scanned: ' + content})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


class ScannerLoginForm(forms.Form):
    name = forms.CharField(max_length=255)
    pin = forms.CharField(max_length=6, widget=forms.PasswordInput)


def scanner_login(request):
    if request.method == 'POST':
        form = ScannerLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            pin = form.cleaned_data['pin']

            try:
                scanner = Scanner.objects.get(name=name, pin=pin)
            except Scanner.DoesNotExist:
                scanner = None

            if scanner:
                # Login the user and redirect to the appropriate page
                request.session['scanner_id'] = scanner.id
                return redirect('scan')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = ScannerLoginForm()
    return render(request, 'scan/scanner_login.html', {'form': form})
