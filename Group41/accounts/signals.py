from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer

from django.core.exceptions import ObjectDoesNotExist

def customer_profile(sender, instance, created, **kwargs):
    if created:
        try:
            print("jere2")
            group = Group.objects.get(name='customer')
            instance.groups.add(group)
        except ObjectDoesNotExist:
            print("jere")
            group = Group.objects.create(name='customer')
            instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name=instance.username,
        )
post_save.connect(customer_profile, sender=User)
