# AI Interviewer 🎯

A sophisticated AI-powered interview practice tool built with Python, Pydantic, and Streamlit. Practice your interview skills with AI-generated questions, voice input support, and detailed feedback.

## ✨ Features

### 🎯 Smart Interview Questions
- **AI-Generated Questions**: Tailored to your target position and experience level
- **Multiple Question Types**: Behavioral, technical, situational, and problem-solving questions
- **Difficulty Levels**: Easy, medium, and hard questions to match your skill level
- **Position-Specific**: Questions relevant to software engineering, data science, product management, and more

### 🎤 Voice & Text Input
- **Voice Recording**: Practice with voice responses using advanced speech recognition
- **Text Input**: Type your answers for detailed responses
- **Real-time Transcription**: Whisper-powered speech-to-text with editing capabilities
- **Multiple Audio Formats**: Support for WAV, MP3, M4A, FLAC, and OGG

### 📊 Intelligent Scoring & Feedback
- **AI-Powered Evaluation**: Detailed scoring on multiple criteria
- **Constructive Feedback**: Specific suggestions for improvement
- **Performance Tracking**: Monitor your progress across interview sessions
- **Scoring Criteria**: Clarity, specificity, relevance, structure, and confidence

### 🎭 Customizable Interview Experience
- **Interviewer Personalities**: Choose from professional-friendly, challenging, supportive, formal, or casual styles
- **Session Management**: Start, pause, and resume interview sessions
- **Progress Tracking**: Monitor questions asked, answers given, and overall performance
- **Tips & Hints**: Contextual guidance for different question types

### 🚀 Modern User Interface
- **Streamlit Frontend**: Clean, responsive web interface
- **Real-time Updates**: Live conversation flow and instant feedback
- **Mobile-Friendly**: Responsive design for all devices
- **Dark/Light Themes**: Customizable appearance

## 🏗️ Architecture

### Core Components
- **Configuration Management**: Pydantic-based settings with environment variable support
- **Data Models**: Type-safe data structures for questions, answers, and sessions
- **AI Interviewer**: Google Gemini-powered question generation and conversation
- **Speech Recognition**: OpenAI Whisper integration for voice input
- **Session Management**: Interview session tracking and analytics

### Technology Stack
- **Backend**: Python 3.9+
- **AI Models**: Google Gemini 2.0 Flash, OpenAI Whisper
- **Web Framework**: Streamlit
- **Data Validation**: Pydantic
- **Dependency Management**: Poetry
- **Logging**: Loguru

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Poetry (for dependency management)
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd interviewer-ai
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   poetry run streamlit run streamlit_app.py
   ```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required: Google Gemini API key
INTERVIEWER_GEMINI_API_KEY=your_gemini_api_key_here

# Optional: OpenAI API key (alternative to Gemini)
INTERVIEWER_OPENAI_API_KEY=your_openai_api_key_here

# Optional: Debug mode
INTERVIEWER_DEBUG=false

# Optional: Log level
INTERVIEWER_LOG_LEVEL=INFO
```

## 📖 Usage

### 1. Configure Your Interview
- Select your target position (Software Engineer, Data Scientist, etc.)
- Choose your preferred interviewer style
- Set your experience level
- Select question types and difficulty

### 2. Start an Interview Session
- Click "Start New Interview" to begin
- The AI will generate your first question
- Choose between text or voice input for your answers

### 3. Practice and Improve
- Answer questions thoughtfully with specific examples
- Receive instant feedback and scoring
- Use tips and hints for guidance
- Track your performance over time

### 4. Review and Learn
- Analyze your scores and feedback
- Identify areas for improvement
- Practice with different question types
- Build confidence for real interviews

## 🔧 Configuration

### Interview Settings
- **Question Types**: Behavioral, technical, situational, problem-solving
- **Difficulty Levels**: Easy, medium, hard
- **Session Limits**: Maximum questions per session
- **Scoring Criteria**: Customizable evaluation metrics

### AI Model Settings
- **Temperature**: Control creativity in question generation
- **Max Tokens**: Limit response length
- **Whisper Model**: Choose speech recognition model size
- **Safety Settings**: Content filtering and moderation

### UI Customization
- **Theme**: Light, dark, or auto
- **Layout**: Wide or narrow layout options
- **Features**: Enable/disable audio recording, file upload, etc.

## 🧪 Development

### Project Structure
```
interviewer-ai/
├── interviewerai/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic data models
│   ├── main.py            # Streamlit application
│   ├── interview/
│   │   ├── __init__.py
│   │   └── interviewer.py # AI interviewer logic
│   └── transcribe/
│       ├── __init__.py
│       └── transcriber.py # Speech recognition
├── streamlit_app.py       # Entry point
├── pyproject.toml         # Poetry configuration
└── README.md
```

### Development Setup

1. **Install development dependencies**
   ```bash
   poetry install --with dev
   ```

2. **Run tests**
   ```bash
   poetry run pytest
   ```

3. **Code formatting**
   ```bash
   poetry run black .
   poetry run isort .
   ```

4. **Linting**
   ```bash
   poetry run flake8
   poetry run mypy .
   ```

### Adding New Features

1. **Data Models**: Add new Pydantic models in `models.py`
2. **Configuration**: Extend settings in `config.py`
3. **AI Logic**: Enhance interviewer capabilities in `interviewer.py`
4. **UI Components**: Add new Streamlit components in `main.py`

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints throughout
- Write comprehensive docstrings
- Include unit tests for new features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini**: AI question generation and conversation
- **OpenAI Whisper**: Speech recognition and transcription
- **Streamlit**: Web application framework
- **Pydantic**: Data validation and settings management

## 📞 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the code comments and this README
- **Community**: Join our discussions and share your experience

## 🔮 Roadmap

### Upcoming Features
- [ ] Multi-language support
- [ ] Interview session export
- [ ] Advanced analytics dashboard
- [ ] Custom question banks
- [ ] Interview simulation modes
- [ ] Integration with job platforms

### Performance Improvements
- [ ] Caching for AI responses
- [ ] Optimized audio processing
- [ ] Background task processing
- [ ] Database integration for persistence

---

**Happy Interviewing! 🎯✨**
