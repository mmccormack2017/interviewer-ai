from transformers import pipeline
import numpy as np

class Transcriber:
    def __init__(self):
        self.transcription_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")

    def transcribe(self, audio):
        sr, y = audio
        
        if y.ndim > 1:
            y = y.mean(axis=1)
            
        y = y.astype(np.float32)
        y /= np.max(np.abs(y))

        return self.transcription_pipeline({"sampling_rate": sr, "raw": y})["text"]