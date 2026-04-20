from django.apps import AppConfig

class ComptesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comptes'

    def ready(self):
        from django.contrib.auth.models import Group

        def create_groups(sender, **kwargs):
            Group.objects.get_or_create(name='Lecteur')
            Group.objects.get_or_create(name='Bibliothecaire')

        from django.db.models.signals import post_migrate
        post_migrate.connect(create_groups, sender=self)