import requests
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Annotated
from pathlib import Path
from openai import OpenAI
import json

app = FastAPI()
client = OpenAI(api_key="<OpenAI API KEY>")

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers = {"Authorization": "Bearer <HF API Token>"}

@app.get("/")
async def root():
  return {"message": "Image-to-text API and Text-to-speech API"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
  #return {"filename": file.filename}
  output = text(file.filename)
  return output

def text(filename):
  with open(filename, "rb") as f:
    data = f.read()
  response = requests.post(API_URL, headers=headers, data=data)
  generated_text = response.json()[0]['generated_text']
  speech(generated_text)
  return (Path(__file__).parent / "speech.mp3")

def speech(text: str):
  speech_file_path = Path(__file__).parent / "speech.mp3"
  response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text
  )
  response.stream_to_file(speech_file_path)
