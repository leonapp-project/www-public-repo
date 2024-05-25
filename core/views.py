# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from leonapp.settings import AUTHENTICATION_BACKENDS
from .forms import SignupForm, UserUpdateForm
from .tokens import account_activation_token

User = get_user_model()


@login_required
def temporary_index_redirect_to_focaccine(request):
    return redirect('focaccine')


# class LoginView(TemplateView):
#     template_name = 'login.html'


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if there is an inactive user with the same email
            inactive_users = User.objects.filter(email=email, is_active=False)
            if inactive_users.exists():
                # Delete the inactive user(s)
                inactive_users.delete()

            # Create the new user with is_active=False
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = _('Activate your account')
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'  # Set the content subtype to 'html'
            email.send()
            return HttpResponse(_('Please confirm your email address to complete the registration'))
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend=AUTHENTICATION_BACKENDS[0])
        return redirect('index')
        # return HttpResponse('Thank you for your email confirmation. Now you can log in your account.')
    else:
        return HttpResponse(_('The activation link is invalid!'))  # 'Il link di attivazione non è valido!'


# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             error_message = _('Invalid email or password')  # 'E-mail o password non validi'
#     else:
#         error_message = ''
#     return render(request, 'login.html', {'error_message': error_message})


class MyLoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user based on email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = _('Invalid email or password')
            return render(request, self.template_name, {'error_message': error_message})


# def logout_view(request):
#     logout(request)
#     return redirect('index')


# class ClassInfoView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = User
#     fields = ['class_number', 'class_section']
#     success_url = "/"

#     def get_object(self, queryset=None):
#         """
#         Overridden to return User which class info are to be updated.
#         """
#         return self.request.user

#     def form_valid(self, form):
#         """
#         Check that fields are not blank before saving to database.
#         """
#         for field in self.fields:
#             if form.cleaned_data[field] == '':
#                 form.add_error(field, 'Questo campo è obbligatorio')
#                 return super().form_invalid(form)

#         return super().form_valid(form)

#     def test_func(self):
#         """
#         Disallow User to re-access the page to change class info.
#         """
#         class_fields = [
#             self.request.user.class_number,
#             self.request.user.class_section
#         ]
#         return not all(class_fields)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'profile.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Your profile was successfully updated!'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Add user to the context
        # Add class_number and class_section display values to the context
        context['class_number_display'] = self.request.user.get_class_number_display()
        context['class_section_display'] = self.request.user.get_class_section_display()
        return context
