import gradio as gr
from scipy.io import wavfile
from gradio_client import Client

from interviewerai.transcribe import Transcriber
from interviewerai.interview import Interviewer

transcriber = Transcriber()
interviewer = Interviewer()

def chat(message, history):
    if history == []:
        question = interviewer.generate_behavioral_question()
        return question
    if message['files'] != []:
        samplerate, data = wavfile.read(message['files'][0])
        text = transcriber.transcribe([samplerate, data])
    if message['text'] != '':
        text = message['text']
    judgement = interviewer.judge_answer(history[-1], text)
    question = interviewer.generate_behavioral_question()
    return [judgement, "\nHere is your next question:",question]

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Markdown("<center><h1>Interview Practice</h1></center>")
            gr.ChatInterface(
                chat,
                examples=["Let's interview!"],
                multimodal=True,
                textbox=gr.MultimodalTextbox(
                    interactive=True,
                    file_count="multiple",
                    placeholder="Begin recording your answer...",
                    show_label=False,
                    sources=["microphone"],
                ),
                type="messages"
            )

demo.launch()