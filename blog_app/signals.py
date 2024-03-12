from .models import UserModel, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=UserModel)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('user profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance) 
            profile.save() 
            print('user is updated')  
        except:
            UserProfile.objects.create(user=instance)
            print('profile was not exisy, bit i created one')   
            print('user is updated')    




