"""Enhanced speech-to-text transcription using Whisper."""

import os
import time
import numpy as np
from typing import Optional, Union
import whisper
from loguru import logger

from ..models import AudioInput, TranscriptionResult
from ..config import settings


class Transcriber:
    """Enhanced speech-to-text transcription using OpenAI Whisper."""
    
    def __init__(self):
        """Initialize the transcriber with the specified Whisper model."""
        self.model_name = settings.model.whisper_model
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the Whisper model."""
        try:
            logger.info(f"Loading Whisper model: {self.model_name}")
            self.model = whisper.load_model(self.model_name)
            logger.info(f"Successfully loaded Whisper model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to load Whisper model {self.model_name}: {e}")
            # Fallback to base model
            try:
                logger.info("Falling back to base model")
                self.model = whisper.load_model("base")
            except Exception as fallback_error:
                logger.error(f"Failed to load fallback model: {fallback_error}")
                raise RuntimeError("Could not load any Whisper model")
    
    def transcribe_audio_file(self, audio_file_path: str) -> TranscriptionResult:
        """
        Transcribe an audio file from disk.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            TranscriptionResult with transcribed text and metadata
        """
        start_time = time.time()
        
        try:
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            logger.info(f"Transcribing audio file: {audio_file_path}")
            
            # Use Whisper's built-in audio loading
            result = self.model.transcribe(audio_file_path)
            
            processing_time = time.time() - start_time
            
            return TranscriptionResult(
                text=result["text"].strip(),
                confidence=result.get("confidence", 0.8),
                language=result.get("language", "en"),
                segments=result.get("segments", []),
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error transcribing audio file {audio_file_path}: {e}")
            raise
    
    def transcribe_audio_data(self, audio_input: AudioInput) -> TranscriptionResult:
        """
        Transcribe audio data from memory.
        
        Args:
            audio_input: AudioInput model containing audio data
            
        Returns:
            TranscriptionResult with transcribed text and metadata
        """
        start_time = time.time()
        
        try:
            logger.info("Transcribing audio data from memory")
            
            # Convert audio data to the format Whisper expects
            audio_array = self._prepare_audio_data(audio_input)
            
            # Transcribe using Whisper
            result = self.model.transcribe(audio_array)
            
            processing_time = time.time() - start_time
            
            return TranscriptionResult(
                text=result["text"].strip(),
                confidence=result.get("confidence", 0.8),
                language=result.get("language", "en"),
                segments=result.get("segments", []),
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error transcribing audio data: {e}")
            raise
    
    def transcribe_legacy(self, audio: Union[tuple, list]) -> str:
        """
        Legacy transcription method for backward compatibility.
        
        Args:
            audio: Tuple of (sample_rate, data) or list [sample_rate, data]
            
        Returns:
            Transcribed text as string
        """
        try:
            if isinstance(audio, (tuple, list)) and len(audio) == 2:
                sample_rate, data = audio
                
                # Create AudioInput model
                audio_input = AudioInput(
                    audio_bytes=data.tobytes(),
                    sample_rate=sample_rate,
                    format="wav"
                )
                
                # Use the new transcription method
                result = self.transcribe_audio_data(audio_input)
                return result.text
            else:
                raise ValueError("Audio must be a tuple or list with (sample_rate, data)")
                
        except Exception as e:
            logger.error(f"Error in legacy transcription: {e}")
            raise
    
    def _prepare_audio_data(self, audio_input: AudioInput) -> np.ndarray:
        """
        Prepare audio data for Whisper transcription.
        
        Args:
            audio_input: AudioInput model containing audio data
            
        Returns:
            Numpy array ready for Whisper
        """
        try:
            # Convert bytes back to numpy array
            audio_array = np.frombuffer(audio_input.audio_bytes, dtype=np.float32)
            
            # Reshape if stereo (2 channels)
            if len(audio_array.shape) > 1:
                audio_array = audio_array.mean(axis=1)
            
            # Normalize audio
            if np.max(np.abs(audio_array)) > 0:
                audio_array = audio_array / np.max(np.abs(audio_array))
            
            # Ensure audio is float32
            audio_array = audio_array.astype(np.float32)
            
            return audio_array
            
        except Exception as e:
            logger.error(f"Error preparing audio data: {e}")
            raise
    
    def get_supported_formats(self) -> list:
        """Get list of supported audio formats."""
        return ["wav", "mp3", "m4a", "flac", "ogg"]
    
    def get_model_info(self) -> dict:
        """Get information about the loaded Whisper model."""
        if self.model is None:
            return {"status": "No model loaded"}
        
        return {
            "model_name": self.model_name,
            "model_type": type(self.model).__name__,
            "device": str(self.model.device),
            "is_multilingual": hasattr(self.model, "is_multilingual")
        }
    
    def change_model(self, model_name: str):
        """
        Change the Whisper model being used.
        
        Args:
            model_name: Name of the new Whisper model
        """
        try:
            logger.info(f"Changing Whisper model to: {model_name}")
            self.model_name = model_name
            self._load_model()
            logger.info(f"Successfully changed to model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to change model to {model_name}: {e}")
            raise