from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


from phonenumber_field.modelfields import PhoneNumberField

"""************* Customer User Creation *************"""

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("email should not provide.")
        # Normaliser l'image
        email = self.normalize_email(email)
        # Créer un nouvel user
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True) # is_staff=True
        extra_fields.setdefault('is_superuser', True) # is_superuser=True
        extra_fields.setdefault('is_active', True) # is_active=True

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser should have is_staff as True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser dhaould have is_superuser as True")
        if extra_fields.get('is_active') is not True:
            raise ValueError("Superuser should have is_active as True")
        
        return self.create_user(email, password, **extra_fields)


class CustomerUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = PhoneNumberField(null=True, unique=True)

    USERNAME_FIELD = 'email' # chaque User est Répresenter pas son email
    # Les champs requis lors de la creation un user
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.email