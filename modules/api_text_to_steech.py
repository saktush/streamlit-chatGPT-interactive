from pathlib import Path
from openai import OpenAI
from decouple import config

text = """
Я узнал, что у меня
Есть огромная семья!
И тропинка и лесок,
В поле каждый колосок.
Речка, небо голубое —
это все мое, родное.
Это Родина моя,
Всех люблю на свете я!
"""

client = OpenAI(
    api_key=config("OPENAI_API_KEY")
)

Voice_list = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

for v in Voice_list:
    speech_file_path = Path(__file__).parent / "result" / f"speech_poem_{v}.mp3"
    response = client.audio.speech.create(
      model="tts-1",
      voice=v,
      input=text
    )

    response.stream_to_file(speech_file_path)
