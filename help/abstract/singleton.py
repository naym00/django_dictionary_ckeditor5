from django.db import models
from django.core.exceptions import ValidationError

class SingletonModel(models.Model):
    """Abstract base class for creating singleton models in Django."""
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(f"Only one {self.__class__.__name__} instance can be created.")
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        """Load the singleton instance, creating it if it doesn't exist."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj