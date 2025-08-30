"""Enhanced AI interviewer using Google Gemini with sophisticated prompting and Pydantic models."""

import os
import uuid
import time
from typing import List, Optional, Dict, Any
from datetime import datetime

import google.generativeai as genai
from loguru import logger

from ..models import (
    Question, Answer, Score, ConversationTurn, InterviewSession,
    InterviewRequest, InterviewResponse, QuestionType, InterviewPosition,
    InterviewerPersonality, UserProfile
)
from ..config import settings


class Interviewer:
    """Enhanced AI interviewer with sophisticated prompting and conversation management."""
    
    def __init__(self):
        """Initialize the interviewer with Gemini model and configuration."""
        self.api_key = settings.api.gemini_api_key
        if not self.api_key:
            raise ValueError("Gemini API key not found. Please set INTERVIEWER_GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        
        # Initialize the model with configuration
        generation_config = genai.types.GenerationConfig(
            temperature=settings.model.temperature,
            max_output_tokens=settings.model.max_tokens,
            top_p=0.8,
            top_k=40
        )
        
        self.model = genai.GenerativeModel(
            model_name=settings.model.model_name,
            generation_config=generation_config
        )
        
        # Safety settings for appropriate content
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        self.model = genai.GenerativeModel(
            model_name=settings.model.model_name,
            generation_config=generation_config,
            safety_settings=self.safety_settings
        )
        
        logger.info(f"Initialized Interviewer with model: {settings.model.model_name}")
    
    def start_interview_session(
        self,
        position: InterviewPosition,
        personality: InterviewerPersonality = InterviewerPersonality.PROFESSIONAL_FRIENDLY,
        user_profile: Optional[UserProfile] = None
    ) -> InterviewSession:
        """
        Start a new interview session.
        
        Args:
            position: Target position for the interview
            personality: Interviewer personality style
            user_profile: Optional user profile for personalized questions
            
        Returns:
            New InterviewSession instance
        """
        session_id = str(uuid.uuid4())
        
        session = InterviewSession(
            id=session_id,
            position=position,
            interviewer_personality=personality,
            start_time=datetime.now()
        )
        
        logger.info(f"Started new interview session {session_id} for position: {position}")
        return session
    
    def generate_question(
        self,
        request: InterviewRequest,
        session: InterviewSession,
        context: Optional[str] = None
    ) -> InterviewResponse:
        """
        Generate a new interview question based on the request.
        
        Args:
            request: InterviewRequest with parameters
            session: Current interview session
            context: Additional context for question generation
            
        Returns:
            InterviewResponse with question and additional information
        """
        try:
            # Build the prompt for question generation
            prompt = self._build_question_prompt(request, session, context)
            
            logger.info(f"Generating question for position: {request.position}, type: {request.question_type}")
            
            # Generate the question
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Empty response from AI model")
            
            # Parse the response and create the question
            question = self._parse_question_response(response.text, request)
            
            # Create the interview response
            interview_response = InterviewResponse(
                question=question,
                follow_up_questions=self._generate_follow_up_questions(question, request),
                tips=self._generate_tips(question, request),
                expected_key_points=self._generate_expected_points(question, request)
            )
            
            logger.info(f"Generated question: {question.text[:100]}...")
            return interview_response
            
        except Exception as e:
            logger.error(f"Error generating question: {e}")
            # Return a fallback question
            return self._generate_fallback_question(request)
    
    def conduct_conversational_interview(
        self,
        user_response: str,
        session: InterviewSession,
        last_question: Optional[Question] = None
    ) -> str:
        """
        Conduct a conversational interview based on user response.
        
        Args:
            user_response: User's response to the last question
            session: Current interview session
            last_question: The last question asked (if any)
            
        Returns:
            AI interviewer's response
        """
        try:
            # Build conversation prompt
            prompt = self._build_conversation_prompt(
                user_response, session, last_question
            )
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if not response.text:
                return "I appreciate your response. Let me ask you another question to continue our conversation."
            
            logger.info("Generated conversational response")
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error in conversational interview: {e}")
            return "Thank you for your response. Let's continue with the next question."
    
    def score_answer(
        self,
        question: Question,
        answer: Answer,
        session: InterviewSession
    ) -> Score:
        """
        Score an interview answer using AI evaluation.
        
        Args:
            question: The question that was answered
            answer: The user's answer
            session: Current interview session
            
        Returns:
            Score with detailed feedback
        """
        try:
            # Build scoring prompt
            prompt = self._build_scoring_prompt(question, answer, session)
            
            logger.info(f"Scoring answer for question: {question.id}")
            
            # Generate score
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Empty response from AI model")
            
            # Parse the scoring response
            score = self._parse_scoring_response(response.text, answer.id)
            
            logger.info(f"Scored answer with overall score: {score.overall_score}")
            return score
            
        except Exception as e:
            logger.error(f"Error scoring answer: {e}")
            # Return a default score
            return Score(
                answer_id=answer.id,
                overall_score=5.0,
                criteria_scores={},
                feedback="Unable to score this answer due to an error.",
                suggestions=["Please try to provide a more detailed response next time."]
            )
    
    def _build_question_prompt(
        self,
        request: InterviewRequest,
        session: InterviewSession,
        context: Optional[str] = None
    ) -> str:
        """Build the prompt for question generation."""
        
        personality_traits = {
            InterviewerPersonality.PROFESSIONAL_FRIENDLY: "professional yet warm and encouraging",
            InterviewerPersonality.CHALLENGING: "challenging and thought-provoking",
            InterviewerPersonality.SUPPORTIVE: "supportive and helpful",
            InterviewerPersonality.FORMAL: "formal and business-like",
            InterviewerPersonality.CASUAL: "casual and conversational"
        }
        
        personality = personality_traits.get(session.interviewer_personality, "professional")
        
        prompt = f"""
        You are an expert {personality} interviewer for a {request.position} position.
        
        Generate a {request.question_type or 'behavioral'} interview question that is:
        - Relevant to the {request.position} role
        - {request.difficulty or 'medium'} difficulty level
        - Engaging and thought-provoking
        - Appropriate for the interview context
        
        {f'Focus on: {request.category}' if request.category else ''}
        {f'Context: {context}' if context else ''}
        
        Previous questions in this session: {[turn.question.text for turn in session.conversation_turns]}
        
        Return ONLY the question text, no additional formatting or explanation.
        """
        
        return prompt.strip()
    
    def _build_conversation_prompt(
        self,
        user_response: str,
        session: InterviewSession,
        last_question: Optional[Question] = None
    ) -> str:
        """Build the prompt for conversational responses."""
        
        personality_traits = {
            InterviewerPersonality.PROFESSIONAL_FRIENDLY: "professional yet warm and encouraging",
            InterviewerPersonality.CHALLENGING: "challenging and thought-provoking",
            InterviewerPersonality.SUPPORTIVE: "supportive and helpful",
            InterviewerPersonality.FORMAL: "formal and business-like",
            InterviewerPersonality.CASUAL: "casual and conversational"
        }
        
        personality = personality_traits.get(session.interviewer_personality, "professional")
        
        prompt = f"""
        You are a {personality} interviewer conducting an interview for a {session.position} position.
        
        The candidate just provided this response: "{user_response}"
        
        {f'This was in response to: "{last_question.text}"' if last_question else ''}
        
        Respond in a conversational interview style that:
        1. Acknowledges their response appropriately
        2. Asks a relevant follow-up question or moves to the next topic
        3. Maintains the {personality} tone
        4. Keeps the conversation flowing naturally
        
        Keep your response concise (2-3 sentences) and engaging.
        """
        
        return prompt.strip()
    
    def _build_scoring_prompt(
        self,
        question: Question,
        answer: Answer,
        session: InterviewSession
    ) -> str:
        """Build the prompt for answer scoring."""
        
        criteria = ", ".join(settings.interview.scoring_criteria)
        
        prompt = f"""
        You are an expert interviewer evaluating a candidate's response.
        
        Question: "{question.text}"
        Answer: "{answer.text}"
        Position: {session.position}
        
        Evaluate this answer on a scale of 1-10 based on these criteria: {criteria}
        
        Provide:
        1. Overall score (1-10)
        2. Individual scores for each criterion
        3. Constructive feedback (2-3 sentences)
        4. 2-3 specific suggestions for improvement
        
        Format your response as JSON:
        {{
            "overall_score": <score>,
            "criteria_scores": {{"<criterion>": <score>}},
            "feedback": "<feedback>",
            "suggestions": ["<suggestion1>", "<suggestion2>"]
        }}
        """
        
        return prompt.strip()
    
    def _parse_question_response(self, response_text: str, request: InterviewRequest) -> Question:
        """Parse the AI response into a Question model."""
        
        # Clean the response text
        question_text = response_text.strip().strip('"').strip("'")
        
        return Question(
            id=str(uuid.uuid4()),
            text=question_text,
            type=request.question_type or QuestionType.BEHAVIORAL,
            position=request.position,
            difficulty=request.difficulty or "medium",
            category=request.category or ""
        )
    
    def _parse_scoring_response(self, response_text: str, answer_id: str) -> Score:
        """Parse the AI scoring response into a Score model."""
        
        try:
            # Try to extract JSON from the response
            import json
            import re
            
            # Find JSON-like content in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                
                return Score(
                    answer_id=answer_id,
                    overall_score=float(data.get("overall_score", 5.0)),
                    criteria_scores=data.get("criteria_scores", {}),
                    feedback=data.get("feedback", "No feedback provided"),
                    suggestions=data.get("suggestions", [])
                )
        except Exception as e:
            logger.warning(f"Failed to parse JSON scoring response: {e}")
        
        # Fallback parsing
        return Score(
            answer_id=answer_id,
            overall_score=5.0,
            criteria_scores={},
            feedback="Unable to parse detailed scoring. General feedback: Consider providing more specific examples and structure in your responses.",
            suggestions=["Use the STAR method for behavioral questions", "Provide concrete examples", "Structure your response clearly"]
        )
    
    def _generate_follow_up_questions(self, question: Question, request: InterviewRequest) -> List[str]:
        """Generate follow-up questions based on the main question."""
        # This could be enhanced with AI generation
        return [
            "Can you provide a specific example?",
            "What was the outcome of that situation?",
            "What would you do differently next time?"
        ]
    
    def _generate_tips(self, question: Question, request: InterviewRequest) -> List[str]:
        """Generate tips for answering the question type."""
        tips_map = {
            QuestionType.BEHAVIORAL: [
                "Use the STAR method (Situation, Task, Action, Result)",
                "Provide specific examples from your experience",
                "Focus on your role and contributions"
            ],
            QuestionType.TECHNICAL: [
                "Explain your thought process step by step",
                "Consider edge cases and trade-offs",
                "Be honest about what you don't know"
            ],
            QuestionType.SITUATIONAL: [
                "Understand the problem before jumping to solutions",
                "Consider multiple approaches",
                "Explain your reasoning clearly"
            ]
        }
        
        return tips_map.get(question.type, ["Think before you speak", "Provide concrete examples"])
    
    def _generate_expected_points(self, question: Question, request: InterviewRequest) -> List[str]:
        """Generate expected key points for a good answer."""
        return [
            "Clear problem understanding",
            "Logical approach",
            "Specific examples",
            "Results and outcomes",
            "Learning and growth"
        ]
    
    def _generate_fallback_question(self, request: InterviewRequest) -> InterviewResponse:
        """Generate a fallback question when AI generation fails."""
        
        fallback_questions = {
            QuestionType.BEHAVIORAL: "Tell me about a time when you had to overcome a significant challenge at work.",
            QuestionType.TECHNICAL: "How would you approach debugging a complex system issue?",
            QuestionType.SITUATIONAL: "If you were given a project with unclear requirements, how would you proceed?",
            QuestionType.PROBLEM_SOLVING: "Describe a problem you solved that required creative thinking."
        }
        
        question_type = request.question_type or QuestionType.BEHAVIORAL
        question_text = fallback_questions.get(question_type, fallback_questions[QuestionType.BEHAVIORAL])
        
        question = Question(
            id=str(uuid.uuid4()),
            text=question_text,
            type=question_type,
            position=request.position,
            difficulty=request.difficulty or "medium",
            category=request.category or ""
        )
        
        return InterviewResponse(
            question=question,
            follow_up_questions=[],
            tips=[],
            expected_key_points=[]
        )
    
    def end_interview_session(self, session: InterviewSession) -> InterviewSession:
        """End an interview session and calculate final scores."""
        
        session.end_time = datetime.now()
        
        # Calculate total score if scoring is enabled
        if settings.interview.enable_scoring:
            scored_turns = [turn for turn in session.conversation_turns if turn.score]
            if scored_turns:
                session.total_score = sum(turn.score.overall_score for turn in scored_turns) / len(scored_turns)
        
        logger.info(f"Ended interview session {session.id} with {session.questions_asked} questions")
        return session
    
