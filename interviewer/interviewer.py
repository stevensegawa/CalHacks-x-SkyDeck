import assemblyai as aai
from elevenlabs import generate, stream
from openai import OpenAI
from dotenv import load_dotenv
import os

# Create an assistant for setup
class AI_Assistant:
    def __init__(self):
        load_dotenv()
        aai.settings.api_key = os.getenv("ASSEMBLY_API_KEY")
        self.openai_client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

        self.transcriber = None

        # Prompt
        self.full_transcript = [
            {"role": "system", "content": "Act as my medical doctor and listen to my symptoms, diagnose me, and provide steps for relief. Be resourceful and efficient. Keep responses concise but not overly short."}
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

        # Upload transcript to OpenAI
        response = self.openai_client.chat.completions.create(
            model = "gpt-4o",
            messages = self.full_transcript
        )

        ai_response = response.choices[0].message.content

        # Use text response for audio response
        self.generate_audio(ai_response)

        self.start_transcription()
    
    # Generate audio with ElevenLabs
    def generate_audio(self, text):
        self.full_transcript.append({"role":"assistant", "content": text})
        print(f"\nAI Friend: {text}")

        audio_stream = generate(
            api_key = self.elevenlabs_api_key,
            text = text,
            voice = "Rachel",
            stream = True,
        )

        stream(audio_stream)

if __name__ == "__main__":
    greeting = "Hello, I am an AI doctor, our diagnoser stated you were at high risk for some health concerns. Please let me know your symptoms and I will try to help."
    ai_assistant = AI_Assistant()
    ai_assistant.generate_audio(greeting)
    ai_assistant.start_transcription()