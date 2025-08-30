"""Pydantic models for the AI Interviewer tool."""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from pydantic import BaseModel, Field, validator


class QuestionType(str, Enum):
    """Types of interview questions."""
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    SITUATIONAL = "situational"
    PROBLEM_SOLVING = "problem-solving"
    LEADERSHIP = "leadership"
    CULTURE_FIT = "culture-fit"


class InterviewPosition(str, Enum):
    """Available interview positions."""
    SOFTWARE_ENGINEER = "Software Engineer"
    DATA_SCIENTIST = "Data Scientist"
    PRODUCT_MANAGER = "Product Manager"
    DEVOPS_ENGINEER = "DevOps Engineer"
    FRONTEND_DEVELOPER = "Frontend Developer"
    BACKEND_DEVELOPER = "Backend Developer"
    FULL_STACK_DEVELOPER = "Full Stack Developer"
    ML_ENGINEER = "Machine Learning Engineer"


class InterviewerPersonality(str, Enum):
    """Interviewer personality styles."""
    PROFESSIONAL_FRIENDLY = "professional_friendly"
    CHALLENGING = "challenging"
    SUPPORTIVE = "supportive"
    FORMAL = "formal"
    CASUAL = "casual"


class Question(BaseModel):
    """Model for interview questions."""
    
    id: str = Field(..., description="Unique identifier for the question")
    text: str = Field(..., description="The question text")
    type: QuestionType = Field(..., description="Type of question")
    position: InterviewPosition = Field(..., description="Target position for this question")
    difficulty: str = Field(default="medium", description="Question difficulty level")
    category: str = Field(default="", description="Question category or topic")
    created_at: datetime = Field(default_factory=datetime.now, description="When the question was created")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Answer(BaseModel):
    """Model for interview answers."""
    
    id: str = Field(..., description="Unique identifier for the answer")
    question_id: str = Field(..., description="ID of the question being answered")
    text: str = Field(..., description="The answer text")
    audio_file: Optional[str] = Field(None, description="Path to audio file if recorded")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the answer was given")
    duration_seconds: Optional[float] = Field(None, description="Duration of audio answer in seconds")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Score(BaseModel):
    """Model for scoring interview answers."""
    
    answer_id: str = Field(..., description="ID of the answer being scored")
    overall_score: float = Field(..., ge=0.0, le=10.0, description="Overall score out of 10")
    criteria_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Scores for individual criteria"
    )
    feedback: str = Field(..., description="Detailed feedback on the answer")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")
    scored_at: datetime = Field(default_factory=datetime.now, description="When the scoring was done")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ConversationTurn(BaseModel):
    """Model for a single turn in the conversation."""
    
    id: str = Field(..., description="Unique identifier for this turn")
    question: Question = Field(..., description="The question asked")
    answer: Optional[Answer] = Field(None, description="The answer given (if any)")
    score: Optional[Score] = Field(None, description="Score for this answer (if scored)")
    timestamp: datetime = Field(default_factory=datetime.now, description="When this turn occurred")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class InterviewSession(BaseModel):
    """Model for a complete interview session."""
    
    id: str = Field(..., description="Unique identifier for the session")
    position: InterviewPosition = Field(..., description="Target position for this interview")
    interviewer_personality: InterviewerPersonality = Field(..., description="Personality style of the interviewer")
    start_time: datetime = Field(default_factory=datetime.now, description="When the session started")
    end_time: Optional[datetime] = Field(None, description="When the session ended")
    conversation_turns: List[ConversationTurn] = Field(
        default_factory=list,
        description="All conversation turns in this session"
    )
    total_score: Optional[float] = Field(None, description="Overall session score")
    notes: Optional[str] = Field(None, description="Additional notes about the session")
    
    @property
    def duration_minutes(self) -> Optional[float]:
        """Calculate session duration in minutes."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 60
        return None
    
    @property
    def questions_asked(self) -> int:
        """Get the number of questions asked."""
        return len(self.conversation_turns)
    
    @property
    def answers_given(self) -> int:
        """Get the number of answers given."""
        return len([turn for turn in self.conversation_turns if turn.answer])
    
    @property
    def average_score(self) -> Optional[float]:
        """Calculate average score across all scored answers."""
        scored_turns = [turn for turn in self.conversation_turns if turn.score]
        if not scored_turns:
            return None
        return sum(turn.score.overall_score for turn in scored_turns) / len(scored_turns)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserProfile(BaseModel):
    """Model for user profile and preferences."""
    
    id: str = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="User's name")
    email: Optional[str] = Field(None, description="User's email address")
    target_positions: List[InterviewPosition] = Field(
        default_factory=list,
        description="Positions the user is interested in"
    )
    experience_level: str = Field(default="entry", description="User's experience level")
    preferred_question_types: List[QuestionType] = Field(
        default_factory=list,
        description="Question types the user prefers"
    )
    interview_history: List[str] = Field(
        default_factory=list,
        description="IDs of previous interview sessions"
    )
    created_at: datetime = Field(default_factory=datetime.now, description="When the profile was created")
    last_active: datetime = Field(default_factory=datetime.now, description="Last activity timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class InterviewRequest(BaseModel):
    """Model for requesting a new interview question."""
    
    position: InterviewPosition = Field(..., description="Target position for the question")
    question_type: Optional[QuestionType] = Field(None, description="Specific type of question desired")
    difficulty: Optional[str] = Field(None, description="Desired difficulty level")
    category: Optional[str] = Field(None, description="Specific category or topic")
    context: Optional[str] = Field(None, description="Additional context for question generation")
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        if v and v not in ['easy', 'medium', 'hard']:
            raise ValueError('Difficulty must be easy, medium, or hard')
        return v


class InterviewResponse(BaseModel):
    """Model for AI interviewer responses."""
    
    question: Question = Field(..., description="The generated question")
    follow_up_questions: List[str] = Field(
        default_factory=list,
        description="Suggested follow-up questions"
    )
    tips: List[str] = Field(
        default_factory=list,
        description="Tips for answering this type of question"
    )
    expected_key_points: List[str] = Field(
        default_factory=list,
        description="Key points expected in a good answer"
    )


class AudioInput(BaseModel):
    """Model for audio input data."""
    
    audio_bytes: bytes = Field(..., description="Raw audio data")
    sample_rate: int = Field(..., description="Audio sample rate")
    format: str = Field(default="wav", description="Audio format")
    duration_seconds: Optional[float] = Field(None, description="Duration of the audio")
    
    @validator('sample_rate')
    def validate_sample_rate(cls, v):
        if v <= 0:
            raise ValueError('Sample rate must be positive')
        return v


class TranscriptionResult(BaseModel):
    """Model for speech-to-text transcription results."""
    
    text: str = Field(..., description="Transcribed text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of transcription")
    language: str = Field(default="en", description="Detected language")
    segments: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Detailed transcription segments"
    )
    processing_time: float = Field(..., description="Time taken to process in seconds")
