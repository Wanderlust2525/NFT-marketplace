from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Связь с User
    balance = models.DecimalField('Баланс', max_digits=10, decimal_places=2, default=0.0)
    avatar  = models.ImageField('Изображение профиля', upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"

# Create your models here.
