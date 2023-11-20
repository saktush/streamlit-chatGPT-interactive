from pathlib import Path
from openai import OpenAI
from decouple import config

text = """
Чтобы нам не ошибаться,
Надо правильно прочесть:
Три, четырнадцать, пятнадцать,
Девяносто два и шесть.
Ну и дальше надо знать,
Если мы вас спросим —
Это будет пять, три, пять,
Восемь, девять, восемь.
"""

client = OpenAI(
    api_key=config("OPENAI_API_KEY")
)

Voice_list = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

for v in Voice_list[-2:]:
    speech_file_path = Path(__file__).parent / "result" / f"P_audio_{v}.mp3"
    response = client.audio.speech.create(
      model="tts-1",
      voice=v,
      input=text
    )

    response.stream_to_file(speech_file_path)
