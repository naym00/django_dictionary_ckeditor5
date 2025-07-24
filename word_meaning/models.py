from django.db import models
from word import models as MODELS_WORD
from user import models as MODELS_USER


class WordMeaning(models.Model):
    text = models.CharField(max_length=100)
    word = models.ForeignKey(MODELS_WORD.Word, on_delete=models.CASCADE, related_name='meanings')
    added_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='added_by_meanings')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.id} - {self.text}'