from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pydub import AudioSegment
from static_ffmpeg import add_paths
import uuid
import os

# Makes FFmpeg available on Render
add_paths()

app = FastAPI()


@app.post("/convert")
async def convert_amr_to_wav(file: UploadFile = File(...)):
    # Generate unique file names in /tmp
    input_file = f"/tmp/{uuid.uuid4()}.amr"
    output_file = f"/tmp/{uuid.uuid4()}.wav"

    # Save uploaded AMR file
    with open(input_file, "wb") as f:
        f.write(await file.read())

    # Convert using pydub
    audio = AudioSegment.from_file(input_file, format="amr")
    audio.export(output_file, format="wav")

    # Return file as downloadable response
    return FileResponse(
        output_file,
        media_type="audio/wav",
        filename="output.wav",
        headers={"Content-Disposition": "attachment; filename=output.wav"}
    )
