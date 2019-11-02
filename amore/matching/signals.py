from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Proposal
from django.utils import timezone
from django.conf import settings
import smtplib

@receiver(post_save, sender=Proposal)
def create_profile(sender, instance, created, **kwargs):
    if created:
        mail = smtplib.SMTP('mail.gmail.com', settings.EMAIL_PORT)
        mail.ehlo()
        mail.starttls()

        message = f'{instance.user.profile.name} has proposed to you ! Check out the proposal now to find your amore ...'
        mail.login(setting.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        email = instance.to_user.email

        try:
            mail.sendmail(settings.EMAIL_HOST_USER, email, message)
        except:
            pass

        print("Mail Sent")
        mail.close()
