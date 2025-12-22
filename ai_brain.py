# ai_brain.py

from typing import List, Dict, Any

# Type aliases
Intent = Dict[str, Any]
WardrobeItem = Dict[str, Any]

def extract_intent(text: str) -> List[Intent]:
    """
    Extract all potential intents from user text with confidence scores.
    Returns a list of intent dictionaries.
    """
    text = text.lower()
    intents: List[Intent] = []

    # Keyword-based intents
    if "birthday" in text or "party" in text:
        intents.append({
            "event": "party",
            "formality": "casual",
            "confidence": 0.9
        })

    if "church" in text:
        intents.append({
            "event": "church",
            "formality": "semi-formal",
            "confidence": 0.8
        })

    if "class" in text or "lecture" in text:
        intents.append({
            "event": "class",
            "formality": "formal",
            "confidence": 0.95
        })

    # Default intent if nothing matches
    if not intents:
        intents.append({
            "event": "general",
            "formality": "casual",
            "confidence": 0.6
        })

    return intents

def select_outfits(wardrobe: List[WardrobeItem], intents: List[Intent]) -> List[WardrobeItem]:
    """
    Rank and select outfits based on multiple intents and confidence.
    Returns top 3 matching wardrobe items.
    """
    scored_items: List[tuple[float, WardrobeItem]] = []

    for intent in intents:
        for item in wardrobe:
            score = 0.0
            # Match formality
            if item.get("formality") == intent.get("formality"):
                score += 2.0
            # Match event tags
            if intent.get("event") in item.get("tags", []):
                score += 1.0
            # Multiply by confidence
            score *= intent.get("confidence", 1.0)

            if score > 0:
                scored_items.append((score, item))

    # Sort descending by score
    scored_items.sort(reverse=True, key=lambda x: x[0])

    # Remove duplicates by name
    unique_items = []
    seen_names = set()
    for score, item in scored_items:
        if item["name"] not in seen_names:
            unique_items.append(item)
            seen_names.add(item["name"])

    return unique_items[:3]

# -----------------------------
# Quick test
# -----------------------------
if __name__ == "__main__":
    user_text = "I have a birthday party tonight"

    wardrobe = [
        {
            "name": "Black T-shirt",
            "category": "top",
            "dominant_color": "black",
            "colors": ["black"],
            "season": "summer",
            "formality": "casual",
            "sleeves": "short",
            "tags": ["casual"]
        },
        {
            "name": "Blue Blazer",
            "category": "top",
            "dominant_color": "blue",
            "colors": ["blue"],
            "season": "all",
            "formality": "formal",
            "sleeves": "long",
            "tags": ["formal"]
        },
        {
            "name": "Sneakers",
            "category": "shoes",
            "dominant_color": "white",
            "colors": ["white"],
            "season": "all",
            "formality": "casual",
            "sleeves": "none",
            "tags": ["casual"]
        }
    ]

    intents = extract_intent(user_text)
    results = select_outfits(wardrobe, intents)

    print("Extracted intents:", intents)
    print("Recommended items:", results)
