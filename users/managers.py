from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email


class UserManager(BaseUserManager):
    def email_validator(self, email):
        if email:
            validate_email(email)
        else:
            raise ValueError("Email is not valid!!!")

    def create_user(self, email, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.save(using=self.db)
        return user
