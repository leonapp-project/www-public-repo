from django.urls import path

from .views import FocaccineIndexView, FocaccineTicketQRCodeView, TicketBuy, TicketHistoryView, TicketDetailView
# handler404 = 'myapp.views.custom_404'

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    # path('', IndexView.as_view(), name='index'),
    # path('class-info/', ClassInfoView.as_view(), name='class_info'),
    path('', FocaccineIndexView.as_view(), name='focaccine'),
    path('qrcode/', FocaccineTicketQRCodeView.as_view(), name='focaccine-qrcode'),
    path('buy/', TicketBuy.as_view(), name='focaccine-buy'),
    path('tickets/', TicketHistoryView.as_view(), name='ticket-history'),
    path('<pk>/', TicketDetailView.as_view(), name='focaccine-detail'),
]
