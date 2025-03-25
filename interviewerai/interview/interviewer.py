import google.generativeai as genai
import os

GEMINI_API_KEY = os.environ.get("GEMINI_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class Interviewer:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")
    
    def generate_behavioral_question(self, history):
        print(history)
        if history==[]:
            response = self.model.generate_content("Come up with a behavioral interview question for a data science position at a FAANG company. Give me only the question and no other text.")
        else:
            print(history)
            response = self.model.generate_content(f"Come up with a behavioral interview question for a data science position at a FAANG company. Give me only the question and no other text. Do not repeat questions from the following list: {history}")
        return response.text
    
    def judge_answer(self, question, answer):
        prompt=f"""You are an interviewer at a technology company. You asked the question: {question}\n\n
                    The interviewee provided the following response: {answer}\n\n
                    Score the interviewees response to the question on a scale of 1-10. Keep your judgement short and concise, but detailed.
                    
                    Keep your response shorter than 250 words."""
        response = self.model.generate_content(prompt)
        return response.text
    
