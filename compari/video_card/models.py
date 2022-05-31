from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse


class VideoCard(models.Model):
    # verbose_name - название столбца в Админ панели
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='О товаре')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    cat = ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # вложенный класс для работы с АП
    class Meta:
        verbose_name = 'Видеокарты 30 поколения'  # редактирует название в админ панели
        verbose_name_plural = 'Видеокарты 30 поколения'  # редактирует множ. число в админ панели
        ordering = ['-time_create', 'title']  # по каким критериям сортировка
    

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    # вложенный класс для работы с АП
    class Meta:
        verbose_name = 'Категория'  # редактирует название в админ панели
        verbose_name_plural = 'Категории'  # редактирует множ. число в админ панели
        ordering = ['id']  # по каким критериям сортировка
