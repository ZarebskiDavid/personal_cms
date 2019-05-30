from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Article_category, Photo_category
from django.core.cache import cache

@receiver(post_save, sender=Photo_category)
@receiver(post_delete, sender=Photo_category)
@receiver(post_save, sender=Article_category)
@receiver(post_delete, sender=Article_category)
def refresh_cached_category(sender, instance, using, **kwargs):
    cache.set('{}'.format(type(instance).__name__), type(instance).objects.all())

'''
@receiver(post_save, sender=Category)
def delete_category(sender, instance, using, **kwargs):
    content_type = instance.content_type 
    cache.set('{}_categories'.format(content_type), Category.objects.filter(content_type=content_type))
'''