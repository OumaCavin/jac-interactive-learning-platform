# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Serializers for Code Translation API
"""

from rest_framework import serializers


class CodeTranslationSerializer(serializers.Serializer):
    """
    Serializer for code translation requests.
    """
    source_code = serializers.CharField(
        help_text="Source code to translate"
    )
    source_language = serializers.ChoiceField(
        choices=[
            ('jac', 'JAC'),
            ('python', 'Python')
        ],
        help_text="Source programming language"
    )
    target_language = serializers.ChoiceField(
        choices=[
            ('jac', 'JAC'),
            ('python', 'Python')
        ],
        help_text="Target programming language"
    )
    
    def validate(self, data):
        """Ensure source and target languages are different."""
        if data['source_language'] == data['target_language']:
            raise serializers.ValidationError(
                "Source and target languages must be different"
            )
        return data


class TranslationResultSerializer(serializers.Serializer):
    """
    Serializer for translation results.
    """
    success = serializers.BooleanField()
    translated_code = serializers.CharField()
    source_language = serializers.CharField()
    target_language = serializers.CharField()
    errors = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    warnings = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    metadata = serializers.JSONField(required=False)


class QuickTranslationSerializer(serializers.Serializer):
    """
    Serializer for quick translation requests (without saving to database).
    """
    code = serializers.CharField(
        help_text="Code to translate"
    )
    direction = serializers.ChoiceField(
        choices=[
            ('jac_to_python', 'JAC to Python'),
            ('python_to_jac', 'Python to JAC')
        ],
        help_text="Translation direction"
    )