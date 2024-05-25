from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .base_user import AbstractBaseUser, BaseUserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password


class FixedCharField(models.CharField):
    def db_type(self, connection):
        varchar: str = super().db_type(connection)
        char: str = varchar.replace('varchar', 'char')
        return char


# class User(AbstractUser):
#     CLASS_SECTION_CHOICES = [
#         ("sca", "Scientifico A"),
#         ("scb", "Scientifico B"),
#         ("scc", "Scientifico C"),
#         ("cla", "Classico"),
#         ("spo", "Sportivo")
#     ]

#     CLASS_NUMBER_CHOICES = [
#         ("1", "Prima"),
#         ("2", "Seconda"),
#         ("3", "Terza"),
#         ("4", "Quarta"),
#         ("5", "Quinta")
#     ]

#     class_number = FixedCharField(
#         max_length=1,
#         choices=CLASS_NUMBER_CHOICES,
#         blank=True,
#         default=""
#     )

#     class_section = FixedCharField(
#         max_length=3,
#         choices=CLASS_SECTION_CHOICES,
#         blank=True,
#         default=""
#     )

#     # define the custom permissions
#     # related to User.
#     class Meta:
#         db_table = "utenti"

#         permissions = (
#             ("can_buy_tickets", "Has the authorization to buy focaccine"),
#         )


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    # def with_perm(
    #     self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    # ):
    #     if backend is None:
    #         backends = auth._get_backends(return_tuples=True)
    #         if len(backends) == 1:
    #             backend, _ = backends[0]
    #         else:
    #             raise ValueError(
    #                 "You have multiple authentication backends configured and "
    #                 "therefore must provide the `backend` argument."
    #             )
    #     elif not isinstance(backend, str):
    #         raise TypeError(
    #             "backend must be a dotted import path string (got %r)." % backend
    #         )
    #     else:
    #         backend = auth.load_backend(backend)
    #     if hasattr(backend, "with_perm"):
    #         return backend.with_perm(
    #             perm,
    #             is_active=is_active,
    #             include_superusers=include_superusers,
    #             obj=obj,
    #         )
    #     return self.none()


class User(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    # is_staff = models.BooleanField(
    #     _("staff status"),
    #     default=False,
    #     help_text=_("Designates whether the user can log into this admin site."),
    # )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    CLASS_SECTION_CHOICES = [
        ("sca", "Scientifico A"),
        ("scb", "Scientifico B"),
        ("scc", "Scientifico C"),
        ("cla", "Classico"),
        ("spo", "Sportivo")
    ]

    CLASS_NUMBER_CHOICES = [
        ("1", "1ᵃ"),
        ("2", "2ᵃ"),
        ("3", "3ᵃ"),
        ("4", "4ᵃ"),
        ("5", "5ᵃ")
    ]

    class_number = FixedCharField(
        max_length=1,
        choices=CLASS_NUMBER_CHOICES,
        blank=True,
        default=""
    )

    class_section = FixedCharField(
        max_length=3,
        choices=CLASS_SECTION_CHOICES,
        blank=True,
        default=""
    )

    can_buy_tickets = models.BooleanField(default=False)

    # define the custom permissions
    # related to User.
    class Meta:
        db_table = "utenti"

        # permissions = (
        #     ("can_buy_tickets", "Has the authorization to buy focaccine"),
        # )
