from django.urls import path
from .views import ScanView, validate_qrcode, scanner_login

urlpatterns = [
    path('', ScanView.as_view(), name='scan'),
    path('login/', scanner_login, name='scanner_login'),
    path('validate-qrcode/', validate_qrcode, name='validate_qrcode'),
]