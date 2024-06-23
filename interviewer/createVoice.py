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

if __name__ == "__main__":
    api_key = '82a697aba53c4dad93c2993bfbf920ab'
    text = ""
    audio_bytes = sync_create_voice(api_key, "steven_v2")