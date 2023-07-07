import requests
from fastapi import APIRouter, UploadFile
from service.setting_service import get_open_ai_api

router = APIRouter(
    prefix="/audio",
    tags=["audio"],
    responses={404: {"description": "Not found"}},
)


@router.post("/openai/transcription")
async def openai_audio_transcribe(audio_file: UploadFile):
    headers = {"Authorization": f"Bearer {get_open_ai_api()}"}
    response = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        data={
            "language": "zh",
            "model": "whisper-1",
        },
        headers=headers,
        files={
            "file": (audio_file.filename, await audio_file.read()),
        },
    )
    return response.json()
