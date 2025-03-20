from django.db import models
from django.core.exceptions import ValidationError

from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import UserProfile

class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField('дата добавление', auto_now_add=True)
    updated_at = models.DateTimeField('дата изменения', auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(verbose_name='название', max_length=100, unique=True)

    def __str__(self):
        return f'{self.id}. {self.name}'
    

def example_validation(value):
    if float(value) == 3.3:
        raise ValidationError('Example error')

    return value

class Picture(TimeStampAbstractModel):

    class Meta:        
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-created_at',)


    name = models.CharField('название', max_length=100)
    description = models.CharField('Описание', max_length=255)
    image = models.ImageField(verbose_name='Изображение', upload_to='media/',null=True, blank=True)
    tags = models.ManyToManyField('marketplace.Tag', verbose_name='теги')
    price = models.DecimalField('цена', max_digits=10, decimal_places=2, default=0.0)
    highest_bid = models.DecimalField('цена', max_digits=10, decimal_places=2, default=0.0)
    date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name='Дата изменении', auto_now=True)
    rating = models.DecimalField('Рейтинг', max_digits=2, decimal_places=1,
                                         validators=[MinValueValidator(1), MaxValueValidator(5), example_validation])
    is_published = models.BooleanField('публичность', default=True)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Профиль пользователя')


    def __str__(self):
        return self.name


class Category(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'категория товара'
        verbose_name_plural = 'категории товаров'
        ordering = ('-created_at',)

    name = models.CharField('название', max_length=50)
    image = models.ImageField(verbose_name='Изображение', upload_to='media/',null=True, blank=True)
    icon = models.ImageField(verbose_name='Иконка', upload_to='media/',null=True, blank=True)
    product = models.ForeignKey('marketplace.Picture', models.CASCADE, related_name='category', verbose_name='category')

    def __str__(self):
        return f'{self.name}'





















# Create your models here.
