from django.contrib import admin
from django.utils.safestring import mark_safe

from marketplace.models import Category, Picture, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')



class CategoryInline(admin.TabularInline):

    model = Category
    extra = 1


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_published', 'get_image')
    list_display_links = ('id', 'name',)
    list_filter = ('category', 'tags','rating', 'user', 'is_published',)
    search_fields = ('name', 'description','tags')
    readonly_fields = ('created_at', 'updated_at', 'get_big_image',)
    inlines = [CategoryInline,]

    @admin.display(description='Изображение')
    def get_image(self, item):
        if item.image and item.image.name:  # Проверяем, есть ли файл
            return mark_safe(f'<img src="{item.image.url}" width="100px">')
        return "-" 

    @admin.display(description='Изображение')
    def get_big_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="100%">')
        return '-'
# Register your models here.
