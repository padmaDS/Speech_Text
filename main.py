import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify
load_dotenv()
from moviepy.editor import *
import requests
import json


app = Flask(__name__)

api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

@app.route('/video', methods=['POST'])
def convert_video_audio():
    video_url = request.json['video_url']
            
    url = video_url

    local_filename = "downloaded.mp4"
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        print("video file downloaded successfully.")
    else:
        print("Failed to download video file. Status code:", response.status_code)

    # Load the mp4 file
    video = VideoFileClip("downloaded.mp4")

    # Extract audio from video
    video.audio.write_audiofile("downloaded.mp3")
   
    audio_file= open("downloaded.mp3", "rb")
    translation = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file
    )
    print("hello")
    print(translation.text)

    def get_completion(prompt, model="gpt-4-turbo-2024-04-09"):
        messages = [{"role": "user", "content": prompt}]
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
        return completion.choices[0].message
    
    details = f"""
    You will be provided with speech of Mr. Revanth Reddy, who is Cheif Minister of Telangana. 
    This speech belongs to an election campaign. This is not a spirtual or religious speech.

    pleae correct the below text both in grammer and context to make it more meaning full in the english language.
 
    '''{translation.text}'''

    """

    details1 = f"""
    You will be provided with speech of Mr. Revanth Reddy, who is Cheif Minister of Telangana. 
    This speech belongs to an election campaign. This is not a spirtual or religious speech.

    pleae summarize as an news article, both in grammer and context to make it more meaning full in the english language, without loosing the true essence.

    '''{translation.text}'''

    """

    translation_details = get_completion(details)
    print(translation_details.content)
    # final_output = eng_details.content
    jj = translation_details.content.replace('"', '').replace('\\', '')

    summary_details1 = get_completion(details1)
    print(summary_details1.content)
    # final_output = eng_details.content

    jj = "original:"+translation.text+" Media Summary  : " + summary_details1.content + "******************** Transcript :   *****************************" + translation_details.content 

    # final_output = jj.content.replace('"', '').replace('\\', '')

    return jsonify(jj)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0', port=4050)