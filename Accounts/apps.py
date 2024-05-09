# yourapp/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Accounts'

    def ready(self):
        post_migrate.connect(self.setup_database, sender=self)

    @staticmethod
    @receiver(post_migrate, dispatch_uid="setup_database_signal")
    def setup_database(sender, **kwargs):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.auth import get_user_model
        from django.contrib.contenttypes.models import ContentType

        # Ensure that this is only executed once by using dispatch_uid
        if kwargs.get('using') != 'default':
            return

        # Create the group if it doesn't exist
        product_management_group, created = Group.objects.get_or_create(name='Exporter')

        # Get or create the 'add_product' permission
        content_type = ContentType.objects.get_for_model(get_user_model())
        permission, _ = Permission.objects.get_or_create(
            codename='add_product',
            content_type=content_type,
        )

        # Assign the permission to the group
        product_management_group.permissions.add(permission)
