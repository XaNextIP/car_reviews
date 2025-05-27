from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'

    def ready(self):
        post_migrate.connect(create_default_superuser, sender=self)

def create_default_superuser(sender, **kwargs):
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123!')
        print("Superuser 'admin' создан с паролем 'admin123!'")