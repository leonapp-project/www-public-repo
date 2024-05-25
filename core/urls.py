from django.urls import path
from .views import signup, activate, temporary_index_redirect_to_focaccine, MyLoginView, UserUpdateView
# login_view, logout_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Account urls
    path('signup/', signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Edit account profile urls
    path('profile/', UserUpdateView.as_view(), name='user_profile'),

    # Index urls
    path('', temporary_index_redirect_to_focaccine, name='index'),
]
