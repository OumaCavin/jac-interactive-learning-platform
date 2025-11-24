# Generated migration to fix assessment field issue

from django.db import migrations, models
from django.db.models import Q
from django.apps import apps


def populate_assessment_field(apps, schema_editor):
    """Populate existing AssessmentAttempt rows with a placeholder Assessment."""
    
    # Get the current models from the app registry
    Assessment = apps.get_model('assessments', 'Assessment')
    AssessmentAttempt = apps.get_model('assessments', 'AssessmentAttempt')
    
    # Create a placeholder assessment if it doesn't exist
    placeholder_assessment, created = Assessment.objects.get_or_create(
        title="Placeholder Assessment",
        defaults={
            'description': "Placeholder for existing assessment attempts",
            'type': 'quiz',
            'max_attempts': 1,
            'passing_score': 0
        }
    )
    
    # Update all assessment attempts that don't have an assessment
    updated_count = AssessmentAttempt.objects.filter(
        assessment__isnull=True
    ).update(
        assessment=placeholder_assessment
    )
    
    print(f"Updated {updated_count} assessment attempts with placeholder assessment")


def reverse_populate_assessment_field(apps, schema_editor):
    """Reverse migration - this is not easily reversible."""
    # This would require finding the original assessment data
    # which is not available in this migration context
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0001_initial'),
    ]

    operations = [
        # First, make the field nullable to allow updates
        migrations.AlterField(
            model_name='assessmentattempt',
            name='assessment',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.CASCADE,
                related_name='attempts',
                to='assessments.assessment'
            ),
        ),
        
        # Run the data migration to populate existing rows
        migrations.RunPython(
            populate_assessment_field,
            reverse_populate_assessment_field
        ),
        
        # Now make the field non-nullable again
        migrations.AlterField(
            model_name='assessmentattempt',
            name='assessment',
            field=models.ForeignKey(
                blank=False,
                null=False,
                on_delete=models.CASCADE,
                related_name='attempts',
                to='assessments.assessment'
            ),
        ),
    ]