from django.db import models
from user import models as MODELS_USER
from word import models as MODELS_WORD
from django_ckeditor_5.fields import CKEditor5Field

class Passage(models.Model):
    title = models.CharField(max_length=100)
    content = CKEditor5Field(config_name='extends')
    added_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='added_by_passage')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.id} - {self.title}'
    
class Passageword(models.Model):
    word = models.ForeignKey(MODELS_WORD.Word, on_delete=models.CASCADE, related_name='word_passages')
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name='passage_words')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.id} - {self.passage.title}'

class Userpassage(models.Model):
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='user_passages')
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name='passage_users')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.id} - {self.user.username} - {self.passage.title}'