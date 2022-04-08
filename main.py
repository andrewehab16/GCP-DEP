import json

from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
import io 
import requests




# Workaround for MCIT API
class bufferedReader(io.BufferedReader):
    name="D:\Fake_path\Fake_path\Fake_path\Fake_path.wav"

app=FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def speech_recognition(audio_file):
    # MCIT API url
    url = "http://41.179.247.136:6000/inference"
    
    audio_file_bytes = io.BytesIO(audio_file)
    audio_file_buffered_reader_object = bufferedReader(audio_file_bytes)    
    data = {'file': audio_file_buffered_reader_object} # json object

    r = requests.post(url, files=data)
    response = json.loads(r.text)

    return response['transcript'].strip()

@app.post("/uploadfile/")
async def upload_and_transcribe(file: bytes=File(...)):
    if not file:
        return {"message": "No file sent"}
    else:  
        audio = AudioSegment(file, sample_width=2, frame_rate=8000, channels=1 ) 
        raw_bytes = audio.raw_data

        txt = speech_recognition(raw_bytes)

        # transcribed Text pre-processing
        if "<fil> " in txt:
            txt = txt.replace("<fil> ", "")

        if "<music> " in txt:
            txt = txt.replace("<music> ", "")

        if "<laugh> " in txt:
            txt = txt.replace("<laugh> ", "")
       
        sentiment = "Neutral"
        returned_json = {"Transcript": txt, "Sentiment": sentiment}

        return returned_json
