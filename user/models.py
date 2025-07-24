from django.db import models
from django.contrib.auth.models import AbstractUser
from help.choice import choice as CHOICE
from help.common.generic import ghelp


class User(AbstractUser):
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=ghelp.list_to_tuple(CHOICE.GENDER))
    
    @property
    def full_name(self):
        name = None
        if self.first_name and self.last_name: name = f'{self.first_name} {self.last_name}' 
        else:
            if self.first_name: name = self.first_name
            else:
                if self.last_name: name = self.last_name
        return name
    
    @property
    def short_name(self):
        name = None
        if self.first_name: name = self.first_name
        else:
            if self.last_name: name = self.last_name
        return name

    def __str__(self):
        return f'{self.username} - {self.is_superuser}'
    

class UserFriend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_users')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['user', 'friend']]
    def __str__(self):
        return f'{self.user.username} - {self.friend.username}'
    
class FriendRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requested_tos')
    requested_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_to_users')
    request_message = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['user', 'requested_to']]
    def __str__(self):
        return f'{self.user.username} - {self.requested_to.username}'