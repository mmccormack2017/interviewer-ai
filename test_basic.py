"""Basic tests to verify the AI Interviewer components work correctly."""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all core components can be imported."""
    try:
        from interviewerai.config import settings
        print("✅ Configuration imported successfully")
        
        from interviewerai.models import Question, InterviewPosition, QuestionType
        print("✅ Models imported successfully")
        
        from interviewerai.interview.interviewer import Interviewer
        print("✅ Interviewer imported successfully")
        
        from interviewerai.transcribe.transcriber import Transcriber
        print("✅ Transcriber imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config():
    """Test configuration loading."""
    try:
        from interviewerai.config import settings
        
        # Check that settings are loaded
        assert hasattr(settings, 'interview')
        assert hasattr(settings, 'model')
        assert hasattr(settings, 'api')
        assert hasattr(settings, 'ui')
        
        print("✅ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_models():
    """Test model creation."""
    try:
        from interviewerai.models import Question, InterviewPosition, QuestionType
        
        # Create a sample question
        question = Question(
            id="test-123",
            text="Tell me about a challenging project you worked on.",
            type=QuestionType.BEHAVIORAL,
            position=InterviewPosition.SOFTWARE_ENGINEER,
            difficulty="medium"
        )
        
        assert question.text == "Tell me about a challenging project you worked on."
        assert question.type == QuestionType.BEHAVIORAL
        assert question.position == InterviewPosition.SOFTWARE_ENGINEER
        
        print("✅ Models work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def main():
    """Run all basic tests."""
    print("🧪 Running basic tests for AI Interviewer...\n")
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("Model Test", test_models),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The AI Interviewer is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
