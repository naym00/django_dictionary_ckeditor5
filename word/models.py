from django.db import models
from user import models as MODELS_USER

class ComplexityLevel(models.Model):
    text = models.CharField(max_length=50, unique=True)
    # short_form = models.CharField(max_length=50, unique=True)
    difficulty_level = models.IntegerField(default=1)
    color = models.CharField(max_length=50)
    is_complexity_level = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.id} - {self.difficulty_level} - {self.text}'

class Word(models.Model):
    text = models.CharField(max_length=100, unique=True)
    pronunciation = models.CharField(max_length=100, blank=True, null=True)
    added_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, blank=True, null=True, related_name='added_by_word')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.id} - {self.text}'
    
class UserWord(models.Model):
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='user_words')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='word_users')
    level = models.ForeignKey(ComplexityLevel, on_delete=models.SET_NULL, blank=True, null=True, related_name='level_words')
    right_prediction = models.IntegerField(default=0)
    wrong_prediction = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'word']]
    
    def __str__(self):
        return f'{self.id} - {self.user.username}'
    
# class Confusion(models.Model):
#     user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='user_confusions')
#     text = models.CharField(max_length=100, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f'{self.id} - {self.user.username}'
    
# class ConfusionWord(models.Model):
#     confusion = models.ForeignKey(Confusion, on_delete=models.CASCADE, related_name='confusion_words')
#     word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='word_confusion_words')
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f'{self.id} - {self.confusion.user.username}'