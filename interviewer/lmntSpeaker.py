import asyncio
from lmnt.api import Speech
import simpleaudio as sa
import io

async def async_generate_voice(api_key, text, voice_id):
    async with Speech(api_key) as speech:
        audio_bytes = await speech.synthesize(text, voice_id, format="wav")
        return audio_bytes["audio"]

def sync_generate_voice(api_key, text, voice_id):
    return asyncio.run(async_generate_voice(api_key, text, voice_id))

def play_audio(audio_bytes):
    # Play the audio using simpleaudio
    wave_obj = sa.WaveObject.from_wave_file(io.BytesIO(audio_bytes))
    play_obj = wave_obj.play()
    play_obj.wait_done()

def playStevenVoice(text):
    api_key = '82a697aba53c4dad93c2993bfbf920ab'
    audio_bytes = sync_generate_voice(api_key, text, "12857976-c707-48ef-bdfe-b610e55ec667")
    play_audio(audio_bytes)