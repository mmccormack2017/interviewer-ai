"""Main Streamlit application for the AI Interviewer tool."""

import streamlit as st
import uuid
import json
from datetime import datetime
from typing import Optional, List
import tempfile
import os

from .config import settings
from .models import (
    InterviewPosition, QuestionType, InterviewerPersonality,
    InterviewRequest, UserProfile
)
from .interview.interviewer import Interviewer
from .transcribe.transcriber import Transcriber


def main():
    """Main Streamlit application."""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title=settings.ui.page_title,
        page_icon=settings.ui.page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "interviewer" not in st.session_state:
        st.session_state.interviewer = None
    if "transcriber" not in st.session_state:
        st.session_state.transcriber = None
    if "current_session" not in st.session_state:
        st.session_state.current_session = None
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = None
    
    # Initialize components
    initialize_components()
    
    # Main application
    render_header()
    render_sidebar()
    
    # Main content area
    if st.session_state.current_session is None:
        render_welcome_screen()
    else:
        render_interview_interface()


def initialize_components():
    """Initialize the interviewer and transcriber components."""
    try:
        if st.session_state.interviewer is None:
            with st.spinner("Initializing AI Interviewer..."):
                st.session_state.interviewer = Interviewer()
                st.success("AI Interviewer initialized successfully!")
        
        if st.session_state.transcriber is None:
            with st.spinner("Initializing Speech Recognition..."):
                st.session_state.transcriber = Transcriber()
                st.success("Speech recognition initialized successfully!")
                
    except Exception as e:
        st.error(f"Failed to initialize components: {e}")
        st.stop()


def render_header():
    """Render the application header."""
    st.markdown(
        f"""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #1f77b4; margin-bottom: 0.5rem;">
                {settings.ui.page_title} 🎯
            </h1>
            <p style="color: #666; font-size: 1.1rem; margin: 0;">
                Practice your interview skills with AI-powered feedback
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()


def render_sidebar():
    """Render the sidebar with configuration options."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Interview settings
        st.subheader("Interview Settings")
        selected_position = st.selectbox(
            "Target Position",
            options=[pos.value for pos in InterviewPosition],
            index=0
        )
        
        selected_personality = st.selectbox(
            "Interviewer Style",
            options=[pers.value for pers in InterviewerPersonality],
            index=0
        )
        
        selected_question_type = st.selectbox(
            "Question Type",
            options=["Any"] + [qt.value for qt in QuestionType],
            index=0
        )
        
        selected_difficulty = st.selectbox(
            "Difficulty Level",
            options=["Any", "easy", "medium", "hard"],
            index=1
        )
        
        # User profile
        st.subheader("👤 User Profile")
        user_name = st.text_input("Your Name", value="")
        user_email = st.text_input("Email (optional)", value="")
        experience_level = st.selectbox(
            "Experience Level",
            options=["entry", "mid-level", "senior", "expert"],
            index=0
        )
        
        # Save profile button
        if st.button("💾 Save Profile"):
            if user_name:
                st.session_state.user_profile = UserProfile(
                    id=str(uuid.uuid4()),
                    name=user_name,
                    email=user_email if user_email else None,
                    target_positions=[InterviewPosition(selected_position)],
                    experience_level=experience_level,
                    preferred_question_types=[QuestionType(selected_question_type)] if selected_question_type != "Any" else []
                )
                st.success("Profile saved!")
            else:
                st.error("Please enter your name to save the profile.")
        
        # Start new interview button
        if st.button("🚀 Start New Interview", type="primary"):
            start_new_interview(
                position=InterviewPosition(selected_position),
                personality=InterviewerPersonality(selected_personality),
                question_type=QuestionType(selected_question_type) if selected_question_type != "Any" else None,
                difficulty=selected_difficulty if selected_difficulty != "Any" else None
            )
        
        # End current interview button
        if st.session_state.current_session and st.button("🏁 End Interview"):
            end_current_interview()
        
        # Display current session info
        if st.session_state.current_session:
            st.subheader("📊 Current Session")
            session = st.session_state.current_session
            st.info(f"Position: {session.position.value}")
            st.info(f"Questions: {session.questions_asked}")
            if session.average_score:
                st.info(f"Avg Score: {session.average_score:.1f}/10")


def render_welcome_screen():
    """Render the welcome screen when no interview is active."""
    st.markdown(
        """
        <div style="text-align: center; padding: 3rem 0;">
            <h2 style="color: #2c3e50; margin-bottom: 2rem;">
                Welcome to AI Interview Practice! 🎉
            </h2>
            <p style="font-size: 1.2rem; color: #555; margin-bottom: 2rem;">
                Prepare for your next job interview with our AI-powered practice tool.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem;">
                <h3>🎯 Smart Questions</h3>
                <p>AI-generated questions tailored to your target position and experience level.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem;">
                <h3>🎤 Voice Input</h3>
                <p>Practice with voice responses using advanced speech recognition technology.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem;">
                <h3>📊 Instant Feedback</h3>
                <p>Get detailed scoring and improvement suggestions for every answer.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Quick start section
    st.markdown("---")
    st.subheader("🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("1. **Configure your interview settings** in the sidebar")
        st.markdown("2. **Choose your target position** and preferred question types")
        st.markdown("3. **Set your experience level** for appropriate questions")
    
    with col2:
        st.markdown("4. **Click 'Start New Interview'** to begin")
        st.markdown("5. **Answer questions** using text or voice input")
        st.markdown("6. **Review feedback** and improve your skills")
    
    # Sample questions preview
    st.markdown("---")
    st.subheader("💡 Sample Questions")
    
    sample_questions = [
        "Tell me about a time when you had to overcome a significant challenge at work.",
        "How would you approach debugging a complex system issue?",
        "Describe a situation where you had to work with a difficult team member.",
        "What's your process for learning new technologies quickly?"
    ]
    
    for i, question in enumerate(sample_questions, 1):
        st.markdown(f"**{i}.** {question}")


def render_interview_interface():
    """Render the main interview interface."""
    session = st.session_state.current_session
    
    # Session header
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader(f"🎯 Interview: {session.position.value}")
    
    with col2:
        st.metric("Questions", session.questions_asked)
    
    with col3:
        if session.average_score:
            st.metric("Avg Score", f"{session.average_score:.1f}/10")
        else:
            st.metric("Avg Score", "N/A")
    
    st.divider()
    
    # Main interview area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_interview_conversation()
    
    with col2:
        render_interview_controls()
        render_tips_and_feedback()


def render_interview_conversation():
    """Render the interview conversation area."""
    st.subheader("💬 Interview Conversation")
    
    # Display conversation history
    for turn in st.session_state.conversation_history:
        with st.container():
            # Question
            st.markdown(f"**🤖 Interviewer:** {turn['question']}")
            
            # Answer (if provided)
            if turn.get('answer'):
                st.markdown(f"**👤 You:** {turn['answer']}")
                
                # Score (if available)
                if turn.get('score'):
                    score = turn['score']
                    st.markdown(f"**📊 Score: {score['overall_score']}/10**")
                    st.markdown(f"**Feedback:** {score['feedback']}")
                    
                    if score.get('suggestions'):
                        st.markdown("**Suggestions:**")
                        for suggestion in score['suggestions']:
                            st.markdown(f"• {suggestion}")
            
            st.divider()
    
    # Current question input
    if st.session_state.conversation_history:
        st.subheader("💭 Your Answer")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["Text Input", "Voice Recording"],
            horizontal=True
        )
        
        if input_method == "Text Input":
            user_answer = st.text_area(
                "Type your answer here:",
                height=150,
                placeholder="Share your thoughts, experiences, and examples..."
            )
            
            if st.button("📤 Submit Answer", type="primary"):
                if user_answer.strip():
                    process_user_answer(user_answer)
                else:
                    st.warning("Please provide an answer before submitting.")
        
        else:  # Voice Recording
            render_voice_recording()


def render_voice_recording():
    """Render the voice recording interface."""
    st.markdown("**🎤 Voice Recording**")
    
    # Audio recorder
    audio_bytes = st.audio_recorder(
        text="Click to record your answer",
        recording_color="#e74c3c",
        neutral_color="#6c757d",
        icon_name="microphone",
        icon_size="2x"
    )
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        if st.button("🎯 Transcribe & Submit"):
            with st.spinner("Transcribing your audio..."):
                try:
                    # Save audio to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_file.write(audio_bytes)
                        tmp_file_path = tmp_file.name
                    
                    # Transcribe
                    transcription = st.session_state.transcriber.transcribe_audio_file(tmp_file_path)
                    
                    # Clean up temporary file
                    os.unlink(tmp_file_path)
                    
                    # Display transcription
                    st.success("Audio transcribed successfully!")
                    st.markdown(f"**Transcription:** {transcription.text}")
                    
                    # Allow editing
                    edited_answer = st.text_area(
                        "Edit transcription if needed:",
                        value=transcription.text,
                        height=100
                    )
                    
                    if st.button("📤 Submit Transcribed Answer"):
                        if edited_answer.strip():
                            process_user_answer(edited_answer)
                        else:
                            st.warning("Please provide an answer before submitting.")
                    
                except Exception as e:
                    st.error(f"Transcription failed: {e}")


def render_interview_controls():
    """Render interview control buttons."""
    st.subheader("🎮 Interview Controls")
    
    # Generate new question
    if st.button("❓ New Question", type="primary", use_container_width=True):
        generate_new_question()
    
    # Skip current question
    if st.button("⏭️ Skip Question", use_container_width=True):
        skip_current_question()
    
    # Get hints
    if st.button("💡 Get Hints", use_container_width=True):
        show_hints()
    
    # Session statistics
    st.subheader("📈 Session Stats")
    
    session = st.session_state.current_session
    st.metric("Duration", f"{session.duration_minutes:.1f} min" if session.duration_minutes else "Active")
    st.metric("Questions Asked", session.questions_asked)
    st.metric("Answers Given", session.answers_given)
    
    if session.average_score:
        st.metric("Performance", f"{session.average_score:.1f}/10")


def render_tips_and_feedback():
    """Render tips and feedback section."""
    st.subheader("💡 Tips & Feedback")
    
    if st.session_state.conversation_history:
        # Show tips for current question type
        current_question = st.session_state.conversation_history[-1]['question']
        
        st.markdown("**General Tips:**")
        if "behavioral" in current_question.lower():
            st.markdown("• Use the STAR method (Situation, Task, Action, Result)")
            st.markdown("• Provide specific examples from your experience")
            st.markdown("• Focus on your role and contributions")
        elif "technical" in current_question.lower():
            st.markdown("• Explain your thought process step by step")
            st.markdown("• Consider edge cases and trade-offs")
            st.markdown("• Be honest about what you don't know")
        else:
            st.markdown("• Think before you speak")
            st.markdown("• Provide concrete examples")
            st.markdown("• Structure your response clearly")
    
    # Recent feedback
    st.subheader("📊 Recent Feedback")
    
    recent_scores = [turn for turn in st.session_state.conversation_history if turn.get('score')]
    
    if recent_scores:
        for turn in recent_scores[-3:]:  # Show last 3 scores
            score = turn['score']
            st.markdown(f"**Score: {score['overall_score']}/10**")
            st.markdown(f"*{score['feedback']}*")
            st.divider()
    else:
        st.info("Complete your first answer to see feedback!")


def start_new_interview(
    position: InterviewPosition,
    personality: InterviewerPersonality,
    question_type: Optional[QuestionType] = None,
    difficulty: Optional[str] = None
):
    """Start a new interview session."""
    try:
        # Create new session
        session = st.session_state.interviewer.start_interview_session(
            position=position,
            personality=personality
        )
        
        st.session_state.current_session = session
        st.session_state.conversation_history = []
        
        # Generate first question
        generate_new_question()
        
        st.success(f"Started new interview for {position.value} position!")
        st.rerun()
        
    except Exception as e:
        st.error(f"Failed to start interview: {e}")


def generate_new_question():
    """Generate a new interview question."""
    try:
        session = st.session_state.current_session
        
        # Create interview request
        request = InterviewRequest(
            position=session.position,
            question_type=None,  # Let AI choose
            difficulty=None,     # Let AI choose
            category=""
        )
        
        # Generate question
        response = st.session_state.interviewer.generate_question(request, session)
        
        # Add to conversation history
        turn = {
            'id': str(uuid.uuid4()),
            'question': response.question.text,
            'answer': None,
            'score': None,
            'timestamp': datetime.now()
        }
        
        st.session_state.conversation_history.append(turn)
        
        st.success("New question generated!")
        st.rerun()
        
    except Exception as e:
        st.error(f"Failed to generate question: {e}")


def process_user_answer(answer_text: str):
    """Process and score a user's answer."""
    try:
        if not st.session_state.conversation_history:
            st.error("No active question to answer!")
            return
        
        # Get current question
        current_turn = st.session_state.conversation_history[-1]
        
        # Update turn with answer
        current_turn['answer'] = answer_text
        
        # Score the answer if scoring is enabled
        if settings.interview.enable_scoring:
            with st.spinner("Scoring your answer..."):
                # This would require creating proper Question and Answer models
                # For now, we'll create a simple score
                score = {
                    'overall_score': 7.5,  # Placeholder
                    'feedback': "Good answer! Consider providing more specific examples next time.",
                    'suggestions': [
                        "Use concrete examples from your experience",
                        "Structure your response more clearly",
                        "Explain the impact of your actions"
                    ]
                }
                current_turn['score'] = score
        
        st.success("Answer submitted successfully!")
        st.rerun()
        
    except Exception as e:
        st.error(f"Failed to process answer: {e}")


def skip_current_question():
    """Skip the current question."""
    if st.session_state.conversation_history:
        current_turn = st.session_state.conversation_history[-1]
        current_turn['answer'] = "[Skipped]"
        current_turn['score'] = None
        st.info("Question skipped. Generating new question...")
        generate_new_question()


def show_hints():
    """Show hints for the current question."""
    if st.session_state.conversation_history:
        current_question = st.session_state.conversation_history[-1]['question']
        
        st.info("**💡 Hints for your question:**")
        
        if "behavioral" in current_question.lower():
            st.markdown("• Think of a specific situation from your work experience")
            st.markdown("• Use the STAR method to structure your response")
            st.markdown("• Focus on what you learned and how you grew")
        elif "technical" in current_question.lower():
            st.markdown("• Break down the problem into smaller parts")
            st.markdown("• Explain your reasoning step by step")
            st.markdown("• Consider different approaches and trade-offs")
        else:
            st.markdown("• Take a moment to think before responding")
            st.markdown("• Provide concrete examples")
            st.markdown("• Be honest about your experience level")


def end_current_interview():
    """End the current interview session."""
    try:
        session = st.session_state.current_session
        
        # End the session
        ended_session = st.session_state.interviewer.end_interview_session(session)
        
        # Display final results
        st.success("Interview completed!")
        
        # Show final statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Questions", ended_session.questions_asked)
        
        with col2:
            st.metric("Final Score", f"{ended_session.total_score:.1f}/10" if ended_session.total_score else "N/A")
        
        with col3:
            st.metric("Duration", f"{ended_session.duration_minutes:.1f} min" if ended_session.duration_minutes else "N/A")
        
        # Reset session state
        st.session_state.current_session = None
        st.session_state.conversation_history = []
        
        st.rerun()
        
    except Exception as e:
        st.error(f"Failed to end interview: {e}")


if __name__ == "__main__":
    main()
