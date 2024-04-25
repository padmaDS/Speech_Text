

import whisper
import gradio as gr 
import os
import sys
import subprocess



input_video = r'data\jeevan reddy.mp4'
def video2mp3(video_file, output_ext="mp3"):
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT, shell = True)
    filename = "jj"
    return f"{filename}.{output_ext}"

audio_file = video2mp3(input_video)

print(audio_file)

# from IPython.display import Audio
# Audio(audio_file)