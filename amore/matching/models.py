from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Proposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    message = models.TextField(max_length=200)
    sent_at = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('proposal_home', kwargs={'pk': self.pk})

class Relationship(models.Model):
    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE, related_name='proposal')
    started_at = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse('relationship_home', kwargs={'pk': self.pk})


# Create your models here.
