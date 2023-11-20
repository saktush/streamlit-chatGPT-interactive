import threading
from pathlib import Path
from openai import OpenAI
from decouple import config

# Test text variable
test_text = """
Hello, darkness, my old friend,
I've come to talk with you again
Because a vision softly creeping,
Left its seeds while I was sleeping,
And the vision that was planted in my brain
Still remains within the sound of silence.
"""
Voice_list = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# initialize openai client
client = OpenAI(api_key=config("OPENAI_API_KEY"))


def generate_speech(voice, text, name_prefix="text") -> None:
    speech_file_path = (
        Path(__file__).parent / "result" / f"{name_prefix}_audio_{voice}.mp3"
    )
    response = client.audio.speech.create(
        model="tts-1-hd", voice=voice, input=text, speed=1
    )
    response.stream_to_file(speech_file_path)


# Create a lock to ensure only one thread is active at a time
thread_lock = threading.Lock()


for v in Voice_list:
    # Acquire the lock before starting the thread
    with thread_lock:
        # Start a thread for each voice
        thread = threading.Thread(
            target=generate_speech,
            args=(v, test_text, "EN"),
        )
        thread.start()

    # Wait for the thread to finish before moving to the next iteration
    thread.join()
