import secrets

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import TimestampModelMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username: str, password: str, **extra_fields: dict) -> "User":
        """Create and save a user with the given username, email, and
        password."""
        if not username:
            raise ValueError("The given username must be set.")

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, password: str, **extra_fields) -> "User":  # type: ignore
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username: str, password: str, **extra_fields) -> "User":  # type: ignore
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimestampModelMixin):
    objects = UserManager()

    MIN_LENGTH_USERNAME = 1
    MAX_LENGTH_USERNAME = 20
    username = models.CharField(
        _("username"),
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
    )

    api_key = models.CharField(_("api key"), max_length=60, default=secrets.token_urlsafe)
    get_questions_count = models.IntegerField(_("get questions count"), default=0)
    DEFAULT_MAX_GET_QUESTIONS_COUNT = 150
    max_get_questions_count = models.IntegerField(
        _("max get questions count"), default=DEFAULT_MAX_GET_QUESTIONS_COUNT
    )

    # permissions
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]

    @property
    def can_get_questions(self) -> bool:
        if self.is_superuser or self.is_admin:
            return True
        return self.get_questions_count < self.max_get_questions_count
