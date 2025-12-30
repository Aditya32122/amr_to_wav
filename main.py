from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from static_ffmpeg import add_paths
from pydub import AudioSegment
import uuid
import os

app = FastAPI()

# Add ffmpeg binary to PATH
add_paths()
AudioSegment.converter = "ffmpeg"


@app.post("/convert-amr-to-wav/")
async def convert_amr_to_wav(file: UploadFile = File(...)):
    input_name = f"{uuid.uuid4()}.amr"
    output_name = f"{uuid.uuid4()}.wav"

    with open(input_name, "wb") as f:
        f.write(await file.read())

    audio = AudioSegment.from_file(input_name, format="amr")
    audio.export(output_name, format="wav")

    os.remove(input_name)

    return FileResponse(output_name, media_type="audio/wav", filename="converted.wav")


@app.post("/convert-amr-to-mp4/")
async def convert_amr_to_mp4(file: UploadFile = File(...)):
    input_name = f"{uuid.uuid4()}.amr"
    output_name = f"{uuid.uuid4()}.mp4"

    with open(input_name, "wb") as f:
        f.write(await file.read())

    audio = AudioSegment.from_file(input_name, format="amr")
    audio.export(output_name, format="mp4")

    os.remove(input_name)

    return FileResponse(output_name, media_type="video/mp4", filename="converted.mp4")
