from django.db import models
from user import models as MODELS_USER

class Forgotpassword(models.Model):
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='user_forgotpassword')
    otp = models.CharField(max_length=5, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.otp}'