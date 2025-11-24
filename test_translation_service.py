"""
Test script for the JAC ↔ Python translation functionality
"""

import sys
import os

# Add the backend path to sys.path
sys.path.append('/workspace/backend')

from apps.jac_execution.services.translator import CodeTranslator, TranslationDirection

def test_translation():
    """Test the translation functionality."""
    print("🔄 Testing JAC ↔ Python Translation Service")
    print("=" * 50)
    
    translator = CodeTranslator()
    
    # Test cases
    test_cases = [
        {
            'name': 'JAC Simple Function',
            'jac_code': '''can greet(name) ->
                print(name)
            ye''',
            'expected_python': '''def greet(name):
    print(name)'''
        },
        {
            'name': 'Python Simple Function',
            'python_code': '''def calculate(a, b):
    result = a + b
    return result''',
            'expected_jac': '''can calculate(a, b) ->
                result = a + b
                return result'''
        },
        {
            'name': 'JAC If Statement',
            'jac_code': '''if age >= 18 ->
                print("Adult")
            else ->
                print("Minor")
            ye''',
            'expected_python': '''if age >= 18:
    print("Adult")
else:
    print("Minor")'''
        }
    ]
    
    # Test JAC to Python translation
    print("🧪 Testing JAC → Python Translation:")
    for test_case in test_cases[:2]:
        print(f"\n📝 Test: {test_case['name']}")
        print(f"Input (JAC):\n{test_case['jac_code']}")
        
        result = translator.translate_code(test_case['jac_code'], TranslationDirection.JAC_TO_PYTHON)
        
        print(f"✅ Success: {result.success}")
        print(f"Output (Python):\n{result.translated_code}")
        
        if result.errors:
            print(f"❌ Errors: {result.errors}")
        if result.warnings:
            print(f"⚠️  Warnings: {result.warnings}")
    
    print("\n" + "=" * 50)
    
    # Test Python to JAC translation
    print("\n🧪 Testing Python → JAC Translation:")
    for test_case in test_cases[1:]:
        print(f"\n📝 Test: {test_case['name']}")
        print(f"Input (Python):\n{test_case['python_code']}")
        
        result = translator.translate_code(test_case['python_code'], TranslationDirection.PYTHON_TO_JAC)
        
        print(f"✅ Success: {result.success}")
        print(f"Output (JAC):\n{result.translated_code}")
        
        if result.errors:
            print(f"❌ Errors: {result.errors}")
        if result.warnings:
            print(f"⚠️  Warnings: {result.warnings}")
    
    print("\n" + "=" * 50)
    print("✅ Translation Service Test Completed!")
    
    return True

if __name__ == "__main__":
    try:
        test_translation()
        print("\n🎉 All translation tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()