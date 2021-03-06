from core.repository import get_clearbit_details

from django.contrib.postgres.fields import JSONField

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                       BaseUserManager, \
                                       PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves new user with email"""

        if not email:
            raise ValueError('User must provide email.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        user.additional_data = get_clearbit_details(email)

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports email"""

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100,
                                  null=False,
                                  blank=True,
                                  default=''
                                  )
    last_name = models.CharField(max_length=30,
                                 null=False,
                                 blank=True,
                                 default='')
    additional_data = JSONField(blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Ingredient(models.Model):
    """Ingredient model"""
    name = models.CharField(max_length=255)


class Recipe(models.Model):
    """Recipe model"""
    name = models.CharField(max_length=255)
    text = models.TextField()
    average_rating = models.DecimalField(max_digits=5,
                                         decimal_places=2,
                                         default=0)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True)
    num_of_ratings=models.IntegerField(default=0)
    total_rating=models.IntegerField(default=0)
    ingredients=models.ManyToManyField(Ingredient)
    num_of_ingredients=models.IntegerField(default=0)

