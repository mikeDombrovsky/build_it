from django.core.files.storage import FileSystemStorage
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from build_it.settings import UPLOAD_ROOT


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def profile(self):
        profile = Profile.objects.get(user=self)


upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    state_region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg', storage=upload_storage)
    verified = models.BooleanField(default=False)
    is_builder = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    services = models.ManyToManyField('Service', related_name='services', blank=True)
    tasks = models.ManyToManyField('Task', related_name='tasks', blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Task(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assignee', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='task_images/', default='no_image.jpg', blank=True, null=True,  storage=upload_storage)

    def __str__(self):
        return self.title + ' - ' + self.customer.email


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    measure = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True, blank=True)
    attachment = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
