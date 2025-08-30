"""Configuration management for the AI Interviewer tool."""

from typing import Optional, List
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class InterviewSettings(BaseSettings):
    """Settings for interview behavior and questions."""
    
    # Interview types and positions
    available_positions: List[str] = Field(
        default=[
            "Software Engineer",
            "Data Scientist", 
            "Product Manager",
            "DevOps Engineer",
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
            "Machine Learning Engineer"
        ],
        description="Available job positions for interview practice"
    )
    
    # Question generation settings
    max_questions_per_session: int = Field(
        default=10,
        description="Maximum number of questions per interview session"
    )
    
    question_types: List[str] = Field(
        default=[
            "behavioral",
            "technical",
            "situational",
            "problem-solving"
        ],
        description="Types of questions to generate"
    )
    
    # Scoring and feedback settings
    enable_scoring: bool = Field(
        default=True,
        description="Whether to enable answer scoring and feedback"
    )
    
    scoring_criteria: List[str] = Field(
        default=[
            "clarity",
            "specificity", 
            "relevance",
            "structure",
            "confidence"
        ],
        description="Criteria for scoring interview answers"
    )
    
    # Conversation settings
    max_conversation_history: int = Field(
        default=20,
        description="Maximum number of conversation turns to remember"
    )
    
    interviewer_personality: str = Field(
        default="professional_friendly",
        description="Personality style of the AI interviewer"
    )


class ModelSettings(BaseSettings):
    """Settings for AI model configuration."""
    
    model_name: str = Field(
        default="gemini-2.0-flash",
        description="Name of the AI model to use"
    )
    
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Creativity level for model responses"
    )
    
    max_tokens: int = Field(
        default=1000,
        description="Maximum tokens for model responses"
    )
    
    # Whisper model settings
    whisper_model: str = Field(
        default="base",
        description="Whisper model size (tiny, base, small, medium, large)"
    )


class APISettings(BaseSettings):
    """API key and endpoint settings."""
    
    gemini_api_key: Optional[str] = Field(
        default=None,
        description="Google Gemini API key"
    )
    
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key (alternative to Gemini)"
    )
    
    # Environment variable mappings
    class Config:
        env_file = ".env"
        env_prefix = "INTERVIEWER_"
        case_sensitive = False


class UISettings(BaseSettings):
    """User interface and experience settings."""
    
    theme: str = Field(
        default="light",
        description="UI theme (light, dark, auto)"
    )
    
    enable_audio_recording: bool = Field(
        default=True,
        description="Enable audio recording functionality"
    )
    
    enable_file_upload: bool = Field(
        default=True,
        description="Enable file upload functionality"
    )
    
    auto_save_conversations: bool = Field(
        default=True,
        description="Automatically save interview conversations"
    )
    
    # Streamlit specific settings
    page_title: str = Field(
        default="AI Interview Practice",
        description="Page title for the Streamlit app"
    )
    
    page_icon: str = Field(
        default="🎯",
        description="Page icon for the Streamlit app"
    )


class Settings(BaseSettings):
    """Main settings class that combines all configuration sections."""
    
    interview: InterviewSettings = Field(
        default_factory=InterviewSettings,
        description="Interview behavior settings"
    )
    
    model: ModelSettings = Field(
        default_factory=ModelSettings,
        description="AI model configuration"
    )
    
    api: APISettings = Field(
        default_factory=APISettings,
        description="API configuration"
    )
    
    ui: UISettings = Field(
        default_factory=UISettings,
        description="User interface settings"
    )
    
    # Global settings
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    class Config:
        env_file = ".env"
        env_prefix = "INTERVIEWER_"
        case_sensitive = False


# Global settings instance
settings = Settings()
