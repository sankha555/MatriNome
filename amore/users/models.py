from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageFile
from django.urls import reverse
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
import requests
from matching.models import Proposal, Relationship

ImageFile.LOAD_TRUNCATED_IMAGES = True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=-1)
    name = models.CharField(max_length=50)

    sex_choices = [('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHERS', 'Rather Not Say'),]
    sex = models.CharField(
        max_length = 20,
        choices = sex_choices,
    )

    birthday = models.DateField(null=True)
    city = models.CharField(max_length=50)
    college = models.CharField(max_length=100)
    interests = models.TextField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    status = models.IntegerField(default=0)
    conquests = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='conquests')
    proposals = models.ManyToManyField(Proposal, blank=True, related_name='proposals')
    relationships = models.ManyToManyField(Relationship, blank=True, related_name='relationships')
    breakups = models.IntegerField(default=0, blank=True)

    def get_age(self):
        return 2019 - self.birthday.year

    def profile_create_url(self):
        return reverse('profile_create', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height>300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




# Create your models here.
