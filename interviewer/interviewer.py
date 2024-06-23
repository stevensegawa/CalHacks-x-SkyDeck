import assemblyai as aai
from openai import OpenAI
from lmnt.api import Speech
from lmntSpeaker import playStevenVoice
import asyncio

# Create an assistant for setup
class AI_Assistant:
    def __init__(self):
        aai.settings.api_key = 'ae4a3f1c60c4401e9fb562c7c320e610'
        self.openai_client = OpenAI(api_key = "sk-proj-sY9f35luVvB3WBqBtnZZT3BlbkFJdeUiFzlLeMqZ4VHA2rTh")
        self.lmnt_api_key = '82a697aba53c4dad93c2993bfbf920ab'
        self.transcriber = None

        # Prompt
        self.full_transcript = [
            # {"role": "system", "content": "You are an AI market researcher. One at a time, ask your interviewee about 1. their age, gender, income level, and purchasing habits 2. any soap brands you know of and their strengths 3. potential products they hope to see in the future. Be resourceful and efficient."}
            {"role": "system", "content": "Act as my medical doctor and listen to my symptoms and try to diagnose me. Be resourceful and efficient."}

        ]

    # Real-time transcription with Assembly AI
    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate = 16000,
            on_data = self.on_data,
            on_error = self.on_error,
            on_open = self.on_open,
            on_close = self.on_close,
            end_utterance_silence_threshold = 2000
        )

        # Connects microphone and streams data to Assembly AI
        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)

    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        # print("Session ID:", session_opened.session_id)
        return


    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")


    def on_error(self, error: aai.RealtimeError):
        # print("An error occured:", error)
        return


    def on_close(self):
        # print("Closing Session")
        return
    
    # Pass real-time transcript to OpenAI
    def generate_ai_response(self, transcript):
        # Stop transcription to allow for response
        self.stop_transcription()

        self.full_transcript.append({"role":"user", "content": transcript.text})
        print(f"\nUser: {transcript.text}", end="\r\n")

        if "oreo" in transcript.text.lower():
            return
        # Upload transcript to OpenAI
        response = self.openai_client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = self.full_transcript
        )

        ai_response = response.choices[0].message.content

        # Use text response for audio response
        self.generate_audio(ai_response)

        self.start_transcription()
    
    # Generate audio with 
    def generate_audio(self, text):
        playStevenVoice(text)

if __name__ == "__main__":
    greeting = "Hello, I am an AI doctor. Let me know your symptoms"
    ai_assistant = AI_Assistant()
    ai_assistant.generate_audio(greeting)
    ai_assistant.start_transcription()