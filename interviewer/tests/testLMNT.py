import asyncio
from lmnt.api import Speech
from pydub import AudioSegment
import simpleaudio as sa
import io


async def async_create_voice(api_key, name):
    async with Speech(api_key) as speech:
        voice = await speech.create_voice(name, True, ['./steven.mp3'])
        voices = await speech.list_voices()
        print(voices)
        return voice

def sync_create_voice(api_key, name):
    return asyncio.run(async_create_voice(api_key, name))

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

async def async_list_voices(api_key):
    async with Speech(api_key) as speech:
        voices = await speech.list_voices()
        return voices

def sync_list_voices(api_key):
    return asyncio.run(async_list_voices(api_key))

if __name__ == "__main__":
    api_key = '82a697aba53c4dad93c2993bfbf920ab'
    text = ""
    audio_bytes = sync_generate_voice(api_key, text, "12857976-c707-48ef-bdfe-b610e55ec667")
    play_audio(audio_bytes)