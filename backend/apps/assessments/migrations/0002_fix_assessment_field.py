# Generated migration to fix assessment field issue

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmentattempt',
            name='assessment',
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=models.CASCADE,
                related_name='attempts',
                to='assessments.assessment'
            ),
        ),
    ]