from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        token = RefreshToken.for_user(user)
        print(
            '''
            Here is a pair of JWT tokens for user: {user}
            refresh token: {refresh}
            access token: {access}
            '''.format(refresh=token, access=token.access_token, user=user)
        )
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields = {'type': 1}
        username = None
        super().create_superuser(username, email, password, **extra_fields)


class CustomUser(AbstractUser):

    ADMIN = 1
    DRIVER = 2
    USER_TYPES = (
        (ADMIN, 'admin'),
        (DRIVER, 'driver'),
    )
    username = None

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    type = models.IntegerField(choices=USER_TYPES, default=DRIVER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return '{1} ({0}) {2}'.format(self.id, self.email, self.get_type_display())

    def __repr__(self):
        return self.__str__()