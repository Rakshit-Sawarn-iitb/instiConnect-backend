from django.db import models

class User(models.Model):

    name = models.CharField(max_length=100)
    username = models.SlugField(default = "@")
    password = models.SlugField(default='0')
    roll_number = models.CharField(max_length=7)
    phone_number = models.CharField(max_length=13)
    email_id = models.EmailField(unique=True, blank=False)
    department = models.CharField(max_length= 50)
    hostel = models.CharField(max_length=10)
    current_year = models.IntegerField()
    date_of_birth = models.DateField()
    connections = models.ManyToManyField('self', blank=True, symmetrical=True, related_name="connected_users")
    connection_requests = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="requested_connections")

    bio = models.TextField(max_length= 500, blank=True)
    no_of_posts = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email_id'
    is_anonymous = False
    is_authenticated = True
    REQUIRED_FIELDS = ['password']
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email_id



