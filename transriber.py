import os
import subprocess
import shutil
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ask user for input file
input_file = input("Enter file name and make sure it's in this directory: ").strip()
output_file = "output.wav"

# If file is mp4 or mov, convert to wav
if input_file.lower().endswith((".mp4", ".mov")):
    command = [
        "ffmpeg", "-i", input_file, "-vn",
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        output_file, "-y"
    ]
    subprocess.run(command, check=True)
else:
    # If it's already audio, ensure we have output.wav
    if input_file != output_file:
        shutil.copy(input_file, output_file)

# Open output.wav and transcribe
with open(output_file, "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file=audio_file
    )

print("Transcript:", transcript.text)
