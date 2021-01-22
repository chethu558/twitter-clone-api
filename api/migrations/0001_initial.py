from django.db import migrations
from api.accounts.models import CustomUser

class Migration(migrations.Migration):
    def seed_data(apps, shcema_editor):
        user = CustomUser(username="Chethan",
                         phone="7975506729",
                         is_staff=True,
                         is_superuser=True)
        
        user.set_password("12345678")
        user.save()

    dependencies = []

    operations = [
         migrations.RunPython(seed_data),
     ]
