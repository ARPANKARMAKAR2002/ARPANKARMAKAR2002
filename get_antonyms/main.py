from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from Word_processor import get_synonyms, get_antonyms, get_definitions

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/process_word")
async def process_word(request: Request):
    data = await request.json()
    word = data.get('word')
    if not word:
        return JSONResponse(status_code=400, content={"message": "Word is required"})
    
    synonyms = get_synonyms(word)
    antonyms = get_antonyms(word)
    definitions = get_definitions(word)
    return {
        'word': word,
        'definitions': definitions,
        'synonyms': synonyms,
        'antonyms': antonyms
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
