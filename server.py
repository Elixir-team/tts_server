from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
import uvicorn
import argparse
import warnings

warnings.simplefilter("ignore")

from tts_service.melo_synthesizer import init_melo_synthesizer
from tts_service.piper_synthesizer import init_piper_synthesizer

parser = argparse.ArgumentParser(description="Speech-to-Text Server")
parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host")
parser.add_argument("--port", type=int, default=8000, help="Server port")
args = parser.parse_args()

melo_model = init_melo_synthesizer()
piper_model = init_piper_synthesizer(exclude=melo_model.supported_languages())
models = [melo_model, piper_model]

app = FastAPI()


# Класс для запроса
class TTSRequest(BaseModel):
    language: str
    text: str


@app.post("/tts/synthesize/")
def generate_tts(request: TTSRequest):
    lang = request.language

    model = next((m for m in models if m.has_lan(lang)), None)

    if model is None: raise HTTPException(status_code=400, detail=f"Language '{lang}' is not supported")

    print(f"🎤 Generate audio ({lang}): {request.text}")
    audio_buffer = model.synthesize(lang, request.text)

    return Response(content=audio_buffer.read(), media_type="audio/wav")


if __name__ == "__main__":
    uvicorn.run(app, host=args.host, port=args.port)
