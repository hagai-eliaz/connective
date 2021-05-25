from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CharField, Manager, TextChoices
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for server."""

    class Types(TextChoices):
        CONSUMER = "CONSUMER", "Consumer"
        COORDINATOR = "COORDINATOR", "Coordinator"
        VENDOR = "VENDOR", "Vendor"

    base_user_type = Types.CONSUMER

    user_type = CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_user_type
    )

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        if not self.id:
            self.user_type = self.base_user_type
        return super().save(*args, **kwargs)


class BaseProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="%(class)s", on_delete=models.CASCADE
    )
    profile_picture = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        abstract = True


class CoordinatorProfile(BaseProfile):
    job_description = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(
        blank=True,
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\d{9,15}$",
                message=_("phone number must be between 9-15 digits"),
            )
        ],
    )


class ConsumerProfile(BaseProfile):
    pass


class VendorProfile(BaseProfile):
    phone_number = models.CharField(
        blank=True,
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\d{9,15}$",
                message=_("phone number must be between 9-15 digits"),
            )
        ],
    )


class ConsumerManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type=User.Types.CONSUMER,
            )
        )


class CoordinatorManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type=User.Types.COORDINATOR,
            )
        )


class VendorManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                user_type=User.Types.VENDOR,
            )
        )


class Consumer(User):
    base_user_type = User.Types.CONSUMER
    objects = ConsumerManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        return self.profile


class Coordinator(User):
    base_user_type = User.Types.COORDINATOR
    objects = CoordinatorManager()

    class Meta:
        proxy = True


class Vendor(User):
    base_user_type = User.Types.VENDOR
    objects = VendorManager()

    class Meta:
        proxy = True
