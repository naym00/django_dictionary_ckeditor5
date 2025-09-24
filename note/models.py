from django.db import models
from user import models as MODELS_USER
from django_ckeditor_5.fields import CKEditor5Field

class Note(models.Model):
    content = CKEditor5Field(config_name='extends')
    added_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='added_by_note')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.id}'
    
class UserNote(models.Model):
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='user_notes')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note_users')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'note']]
    
    def __str__(self):
        return f'{self.id} - {self.user.username}'