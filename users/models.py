from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email_id, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email_id:
            raise ValueError("The Email field must be set")

        email_id = self.normalize_email(email_id)
        user = self.model(email_id=email_id, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email_id, password=None, **extra_fields):
        """Create and return a superuser, filling missing fields with random data."""
        # Set random data for missing fields if not provided
        extra_fields.setdefault('current_year', 4)  # Assuming current_year is between 1 and 4
        extra_fields.setdefault('department', 'IEOR')
        extra_fields.setdefault('phone_number', '1234567890')
        extra_fields.setdefault('name', 'Superuser')
        extra_fields.setdefault('username', 'superuser')
        extra_fields.setdefault('roll_number', '1234567')
        extra_fields.setdefault('date_of_birth', '2000-01-01')
        extra_fields.setdefault('hostel', 'Hostel 1')
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Create and return superuser
        return self.create_user(email_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    username = models.SlugField(default="@", unique=True)
    roll_number = models.CharField(max_length=7)
    phone_number = models.CharField(max_length=13)
    email_id = models.EmailField(unique=True, blank=False)
    department = models.CharField(max_length=50)
    hostel = models.CharField(max_length=10)
    current_year = models.IntegerField()
    date_of_birth = models.DateField()
    connections = models.ManyToManyField('self', blank=True, symmetrical=True, related_name="connected_users")
    connection_requests = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="requested_connections")

    bio = models.TextField(max_length=500, blank=True)
    no_of_posts = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email_id'
    REQUIRED_FIELDS = ['name', 'username']  # ✅ Removed 'password', Django handles it internally

    objects = UserManager()

    def __str__(self):
        return self.email_id
