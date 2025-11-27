# Generated migration for adding generated_by_agent field to AdaptiveChallenge
# This migration adds the generated_by_agent field as nullable to avoid default value issues

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0006_add_missing_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='adaptivechallenge',
            name='generated_by_agent',
            field=models.CharField(blank=True, help_text='Which AI agent generated this', max_length=50, null=True),
        ),
    ]