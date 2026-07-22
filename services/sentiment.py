import json
import torch

from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

ASPECT_MODEL = "Vampire123456/indobert-sentiment"
SENTIMENT_MODEL = "Vampire123456/indobert-absa"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# tokenizer
tokenizer = AutoTokenizer.from_pretrained(ASPECT_MODEL)

# model deteksi aspek
model_aspect = AutoModelForSequenceClassification.from_pretrained(
    ASPECT_MODEL
)
model_aspect.to(device).eval()

# model sentimen
model_sentiment = AutoModelForSequenceClassification.from_pretrained(
    SENTIMENT_MODEL
)
model_sentiment.to(device).eval()

# download label_cols.json dari Hugging Face
label_file = hf_hub_download(
    repo_id=ASPECT_MODEL,
    filename="label_cols.json"
)

with open(label_file, "r") as f:
    ASPECT_LABELS = json.load(f)

LABEL_MAP = {
    0: "positive",
    1: "neutral",
    2: "negative",
}

ASPECT_THRESHOLD = 0.5


def detect_aspects(text: str, threshold: float = ASPECT_THRESHOLD):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = model_aspect(**inputs).logits

    probs = torch.sigmoid(logits).cpu().numpy()[0]

    return [
        {
            "aspect": ASPECT_LABELS[i],
            "prob": float(p),
        }
        for i, p in enumerate(probs)
        if p >= threshold
    ]


def predict_sentiment(aspect: str, text: str):
    input_text = f"[ASPECT] {aspect} [TEXT] {text}"

    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = model_sentiment(**inputs).logits

    probs = torch.softmax(logits, dim=1)

    score, predicted = torch.max(probs, dim=1)

    return {
        "label": LABEL_MAP[predicted.item()],
        "score": float(score.item()),
    }


def analyze_sentiment(komentar: str | None):
    result = {
        asp: None
        for asp in ASPECT_LABELS
    }

    if not komentar or not komentar.strip():
        return result

    detected = detect_aspects(komentar)

    for item in detected:
        aspect = item["aspect"]

        sentiment = predict_sentiment(
            aspect,
            komentar
        )

        sentiment["aspect_confidence"] = item["prob"]

        result[aspect] = sentiment

    return result