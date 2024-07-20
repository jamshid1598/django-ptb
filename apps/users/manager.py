from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, phone, is_staff, is_superuser, password, **extra_fields):
        if not phone:
            raise ValueError('unique username must be required')
        user = self.model(
            phone=phone,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )

        # user.set_unusable_password()
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, phone, password, **extra_fields):
        return self._create_user(phone, False, False, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        return self._create_user(phone, True, True, password, **extra_fields)
