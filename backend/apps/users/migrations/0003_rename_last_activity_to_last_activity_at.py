# Migration to rename last_activity to last_activity_at to match current model definition
# This resolves the field name mismatch causing migration issues

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_fix_user_model_fields'),
    ]

    operations = [
        # Rename last_activity field to last_activity_at to match current model
        migrations.RenameField(
            model_name='user',
            old_name='last_activity',
            new_name='last_activity_at',
        ),
    ]