from django.dispatch import receiver

from Main.models import House
from django.utils.text import slugify
from django.db.models.signals import pre_save


@receiver(pre_save, sender=House)
def pre_save_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title + "-" + instance.created)
