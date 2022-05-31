from django.apps import AppConfig


class VideoCardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_card'
    # verbose_name - название приложения в Админ панели
    verbose_name = 'Видеокарты'
