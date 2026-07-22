from fastapi import FastAPI, HTTPException
from services.sentiment import analyze_sentiment
from models.schema import PredictRequest, BatchRequest

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Sentiment API is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(request: PredictRequest):
    if not request.komentar or not request.komentar.strip():
        raise HTTPException(
            status_code=400,
            detail="Komentar tidak boleh kosong"
        )

    result = analyze_sentiment(request.komentar)
    return result


@app.post("/predict-batch")
async def predict_batch(request: BatchRequest):
    results = [
        analyze_sentiment(item.komentar)
        for item in request.data
    ]
    return results