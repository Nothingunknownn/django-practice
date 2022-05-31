from django.contrib import admin
from .models import *

'''Редактируем админ панель
list_display - колонки которые отображаются в АП
list_display_links - поля-ссылки пересылающие на статью
search_fields - поля по которым можно производить поиск
list_editable - делает поле редактируемым
list_filter - поля по которым мы можем фильтровать
prepopulated_fields - автоматически заполняет slug на основе поля нейм
'''


class VideoCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_link = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


# Register your models here.

admin.site.register(VideoCard, VideoCardAdmin)
admin.site.register(Category, CategoryAdmin)
