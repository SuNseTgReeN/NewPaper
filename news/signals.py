from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from .tasks import send_notifications


@receiver(post_save, sender=Post)
def notify_about_new_post(sender, instance, created, **kwargs):
    if created and instance.__class__.__name__ == 'Post':
        send_notifications.apply_async((instance.preview(), instance.pk, instance.title), countdown=10)
