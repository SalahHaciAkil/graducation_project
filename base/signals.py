# signals.py

from django.db.models.signals import pre_save, post_save

from .models import User

# pre_save is a signal that is sent before a model is saved
# post_save is a signal that is sent after a model is saved
# sender is the model that is sending the signal
# instance is the instance of the model that is sending the signal
# created is a boolean that is true if the instance is being created

def updateUser(sender, instance, **kwargs):
        user = instance
        if user.email != '':
            user.username = user.email


pre_save.connect(updateUser, sender=User)