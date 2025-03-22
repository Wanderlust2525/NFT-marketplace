from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# from marketplace.models import Picture



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Связь с User
    balance = models.DecimalField('Баланс', max_digits=10, decimal_places=2, default=0)
    avatar  = models.ImageField('Изображение профиля', upload_to='avatars/', null=True, blank=True)

    purchased_images = models.ManyToManyField('marketplace.Picture', related_name='buyers', blank=True)

    def __str__(self):
        return f"{self.user.username}"
    
    

    def add_balance(self, amount):
        amount = Decimal(amount)
        self.balance += amount
        self.save()

    def buy_picture(self, picture):
            if self.balance >= picture.price:
                self.balance -= picture.price
                self.save()

                self.purchased_images.add(picture)
                picture.user = self
                picture.save()
                picture.is_published = False  
                picture.save()

                return True
            else:
                return False
                
# Create your models here.
