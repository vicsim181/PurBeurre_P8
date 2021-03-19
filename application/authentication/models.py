# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.db import models


# # Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, first_name=None, last_name=None, is_staff=False,
#                     is_admin=False, is_active=True):
#         if not email:
#             raise ValueError('Vous devez renseigner une adresse email pour vous inscrire.')
#         if not password:
#             raise ValueError('Vous devez renseigner un mot de passe pour vous inscrire.')
#         if not first_name:
#             raise ValueError('Vous devez renseigner un prénom pour vous inscrire.')
#         if not last_name:
#             raise ValueError('Vous devez renseigner un nom de famille pour vous inscrire.')

#         user_obj = self.model(email=self.normalize_email(email))
#         user_obj.set_password(password)
#         user_obj.first_name = first_name
#         user_obj.last_name = last_name
#         user_obj.staff = is_staff
#         user_obj.admin = is_admin
#         user_obj.active = is_active
#         user_obj.save(using=self._db)
#         return user_obj

#     def create_staffuser(self, email, password=None):
#         user = self.create_user(
#             email, password=password, is_staff=True
#         )
#         return user

#     def create_superuser(self, email, password=None):
#         user = self.create_user(
#             email, password=password, is_staff=True, is_admin=True
#         )
#         return user


# class User(AbstractBaseUser):
#     email = models.EmailField(max_length=50, unique=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     active = models.BooleanField(default=True)
#     staff = models.BooleanField(default=False)
#     admin = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     objects = UserManager()

#     def __str__(self) -> str:
#         return self.email

#     def get_full_name(self):
#         if self.full_name:
#             return self.full_name
#         return self.email

#     def get_short_name(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True

#     @property
#     def is_staff(self):
#         return self.staff

#     @property
#     def is_admin(self):
#         return self.admin

#     @property
#     def is_active(self):
#         return self.active
##########################################################################################################
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, is_staff=False,
                    is_admin=False, is_active=True):
        if not email:
            raise ValueError('Vous devez renseigner une adresse email pour vous inscrire.')
        if not password:
            raise ValueError('Vous devez renseigner un mot de passe pour vous inscrire.')
        if not first_name:
            raise ValueError('Vous devez renseigner un prénom pour vous inscrire.')
        if not last_name:
            raise ValueError('Vous devez renseigner un nom de famille pour vous inscrire.')

        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email, password=password, is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email, password=password, is_staff=True, is_admin=True
        )
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
# blank=True, max_length=254, verbose_name='email address',

# class CustomeUserManager(UserManager):
#     def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
