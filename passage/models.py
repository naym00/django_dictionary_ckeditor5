from django.db import models
from help.common.generic import ghelp
from user import models as MODELS_USER
from word import models as MODELS_WORD
from help.choice import choice as CHOICE
from django_ckeditor_5.fields import CKEditor5Field

class Passage(models.Model):
    title = models.CharField(max_length=100)
    content = CKEditor5Field(config_name='extends')
    added_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='added_by_passage')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.id} - {self.title}'
    
class PassageWord(models.Model):
    word = models.ForeignKey(MODELS_WORD.Word, on_delete=models.CASCADE, related_name='word_passages')
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name='passage_words')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['word', 'passage']]
    def __str__(self):
        return f'{self.id} - {self.passage.title}'

class UserPassage(models.Model):
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='user_passages')
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name='passage_users')
    title = models.CharField(max_length=100)
    content = CKEditor5Field(config_name='extends')
    note = CKEditor5Field(config_name='extends')
    audience = models.CharField(max_length=15, choices=ghelp.list_to_tuple(CHOICE.AUDIENCE))
    hide_from_mine_profile = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['user', 'passage']]
    def __str__(self):
        return f'{self.id} - {self.user.username} - {self.title}'
    
class UserPassageShareOnly(models.Model):
    user_passage = models.ForeignKey(UserPassage, on_delete=models.CASCADE, db_index=True, related_name='audience_user_passages')
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='user_audiences')
    class Meta:
        unique_together = [['user_passage', 'user']]
    def __str__(self):
        return f'{self.id} - {self.user_passage.user.username}'