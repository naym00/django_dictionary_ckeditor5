from django.core.exceptions import ValidationError
from help.abstract.singleton import SingletonModel
from django.db.models.signals import pre_delete
from user import models as MODELS_USER
from django.dispatch import receiver
from django.db import models

class Settings(SingletonModel):
    otp_validation_minutes = models.IntegerField(default=2)
    def __str__(self):
        return f'{self.id} - {self.otp_validation_minutes}'

@receiver(pre_delete, sender=Settings)
def prevent_singleton_deletion(sender, instance, **kwargs):
    """Prevent deletion of the singleton instance."""
    raise ValidationError(f"{sender.__name__} instance cannot be deleted!")
    
class UserSettings(models.Model):
    user = models.OneToOneField(MODELS_USER.User, on_delete=models.CASCADE, related_name='user_setting')
    new_word_day_duration = models.IntegerField(default=7)
    words_per_page = models.IntegerField(default=12)
    def __str__(self):
        return f'{self.id} - {self.user.username}'