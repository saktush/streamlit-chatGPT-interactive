from openai import OpenAI
from decouple import config

prompt = """
Happy little bear with big brown nose eats carrot sitting at a grand lake on sunset
"""

client = OpenAI(
    api_key=config("OPENAI_API_KEY")
)

response = client.images.generate(
  model="dall-e-3",
  prompt=prompt,
  size="256x256",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

print(image_url)
