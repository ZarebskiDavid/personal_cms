from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Article_category, Photo_category, Person, Photo, Article
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import F

@receiver(post_save, sender=Photo_category)
@receiver(post_delete, sender=Photo_category)
@receiver(post_save, sender=Article_category)
@receiver(post_delete, sender=Article_category)
def refresh_cached_category(sender, instance, using, **kwargs):
    cache.set('{}'.format(type(instance).__name__), type(instance).objects.all())

# TODO: understand why this line cause "Problem installing fixture" PCQ count est défini au niveau de la classe abstraite?
@receiver(post_save, sender=Article)
@receiver(post_save, sender=Photo)
def add_one_to_count(sender, instance, using, **kwargs):
	cat = type(instance.category).objects.get(name=instance.category)
	cat.count = F('count')+1
	cat.save()
	cache.set('{}_category'.format(sender.__name__), sender.objects.all())

@receiver(post_delete, sender=Article)
@receiver(post_delete, sender=Photo)
def drop_one_to_count(sender, instance, using, **kwargs):
	cat = type(instance.category).objects.get(name=instance.category)
	cat.count = F('count')-1
	cat.save()
	cache.set('{}_category'.format(sender.__name__), sender.objects.all())

@receiver(post_save, sender=User)
def add_new_user_to_persons(sender, instance, **kwargs): 
    p = Person.objects.get_or_create(
        first_name = instance.first_name, 
        last_name  = instance.last_name)
    