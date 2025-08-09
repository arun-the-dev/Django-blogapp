from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
import uuid
from ..helpers import default_expire_time
class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email and not password :
            raise ValueError("Email or Password Required !!!")
        normalized_email = self.normalize_email(email=email)
        user = self.model(email = normalized_email,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        return self.create_user(email=email,password=password,**extra_fields)
class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=255,blank=True)
    last_name =  models.CharField(max_length=255,blank=True)
    profile_pic = models.ImageField(upload_to="user_profile_pics/" ,default="defaults/default_user_profile.jpeg",blank=True)
    email = models.EmailField(unique=True,blank=True)

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email
    @property
    def get_full_name(self):
        return self.first_name+" " + self.last_name

class Otp(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField(default=default_expire_time)
