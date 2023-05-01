from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# AbstractBaseUser를 사용하기 위해 필요한 클래스
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# custom User model을 사용하기 위한 클래스
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    # #symmetrical : 서로 대칭인지 알아보기 위한 것 (True일때  : 팔로우를 걸었을대 상대방의 허락이 필요한경우, False일때 : 상대방과 자신이 마음대로 팔로우를 걸수 있는경우)
    # followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin