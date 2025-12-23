from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional
from PIL import Image
import requests
from io import BytesIO

# Import rule-based brain
from ai_brain import extract_intent, select_outfits

app = FastAPI(
    title="Stylus",
    description="Rule-based outfit recommendation backend",
    version="0.1.0",
)

# -----------------------------
# Models
# -----------------------------
class WardrobeItem(BaseModel):
    name: str
    category: Optional[str] = None
    tags: List[str] = []
    formality: Optional[str] = None
    dominant_color: Optional[str] = None
    colors: Optional[List[str]] = None
    season: Optional[str] = None
    sleeves: Optional[str] = None

class GenerateOutfitRequest(BaseModel):
    text: str
    wardrobe: List[WardrobeItem]

class RecommendedItem(BaseModel):
    name: str
    score: float

class AssistantRequest(BaseModel):
    message: str

class AssistantResponse(BaseModel):
    intent: dict
    action: str
    reasoning: str

class TagItemRequest(BaseModel):
    image_url: HttpUrl

# -----------------------------
# Helper Functions
# -----------------------------
def get_weather(lat: float, lon: float) -> dict:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,precipitation,wind_speed_10m"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        current = response.json().get("current", {})
        temperature = current.get("temperature_2m")
        rain = current.get("precipitation")
        wind = current.get("wind_speed_10m")

        if rain and rain > 0:
            summary = "Rainy"
        elif temperature and temperature > 28:
            summary = "Hot and dry"
        else:
            summary = "Mild weather"

        return {"temperature": temperature, "rain": rain, "wind_speed": wind, "summary": summary}

    except Exception as e:
        return {"error": str(e)}

def load_image_info(url: str) -> dict:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")
        width, height = img.size
        small = img.resize((1,1))
        dominant_color = small.getpixel((0,0))
        return {
            "width": width,
            "height": height,
            "dominant_color": {"r": dominant_color[0], "g": dominant_color[1], "b": dominant_color[2]},
            # Placeholder fields for Week 1 compliance
            "category": "top",
            "formality": "casual",
            "colors": ["red", "blue"],
            "season": "summer",
            "sleeves": "short"
        }
    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# Health Endpoint
# -----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Outfit AI service is running"}

# -----------------------------
# AI Endpoints
# -----------------------------
@app.post("/ai/generate-outfit")
def generate_outfit(payload: GenerateOutfitRequest):
    wardrobe_dicts: List[Dict[str, Any]] = [item.dict() for item in payload.wardrobe]
    intents = extract_intent(payload.text)
    recommended_items = select_outfits(wardrobe_dicts, intents)
    response_items = [{"name": item.get("name"), "score": 1.0} for item in recommended_items]
    return {"intent": intents, "recommended_items": response_items}

@app.post("/ai/tag-item")
def tag_item(payload: TagItemRequest):
    return load_image_info(payload.image_url)

@app.post("/ai/assistant", response_model=AssistantResponse)
def assistant(payload: AssistantRequest):
    intents = extract_intent(payload.message)
    primary_intent = intents[0]  # pick the first intent
    if "event" in primary_intent:
        action = "generate_outfit"
        reasoning = "User is asking for outfit advice for an event"
    else:
        action = "clarify"
        reasoning = "User intent is unclear"
    return {"intent": primary_intent, "action": action, "reasoning": reasoning}

@app.get("/context/weather")
def weather(lat: float, lon: float):
    return get_weather(lat, lon)

@app.post("/ai/classify-event")
def classify_event(payload: AssistantRequest):
    intents = extract_intent(payload.message)
    return {"intents": intents}
