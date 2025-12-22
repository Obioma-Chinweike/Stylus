# ai_brain.py

Intent = dict
WardrobeItem = dict


def extract_intent(text: str) -> list[Intent]:
    """
    Extract all potential intents from text with confidence.
    """
    text = text.lower()
    intents = []

    # Check all keywords
    if "birthday" in text or "party" in text:
        intents.append({"event": "party", "formality": "casual", "confidence": 0.9})

    if "church" in text:
        intents.append({"event": "church", "formality": "semi-formal", "confidence": 0.8})

    if "class" in text or "lecture" in text:
        intents.append({"event": "class", "formality": "formal", "confidence": 0.95})

    # default intent if nothing matched
    if not intents:
        intents.append({"event": "general", "formality": "casual", "confidence": 0.6})

    return intents



def select_outfits(wardrobe: list[WardrobeItem], intents: list[Intent]) -> list[WardrobeItem]:
    """
    Select and rank outfits based on multiple intents and confidence.
    """
    scored_items = []

    for intent in intents:
        for item in wardrobe:
            score = 0
            if intent["formality"] in item["tags"]:
                score += 2
            if intent.get("event") in item.get("tags", []):
                score += 1

            score *= intent.get("confidence", 1.0)

            if score > 0:
                scored_items.append((score, item))

    # sort descending by score and remove duplicates
    scored_items.sort(reverse=True, key=lambda x: x[0])
    unique_items = []
    seen = set()
    for score, item in scored_items:
        if item["name"] not in seen:
            unique_items.append(item)
            seen.add(item["name"])

    return unique_items[:3]



if __name__ == "__main__":
    user_text = "I have a birthday party tonight"

    wardrobe = [
        {"name": "Black T-shirt", "tags": ["casual"]},
        {"name": "Blue Blazer", "tags": ["formal"]},
        {"name": "Sneakers", "tags": ["casual"]}
    ]

    intent = extract_intent(user_text)
    results = select_outfits(wardrobe, intent)

    print("Intent:", intent)
    print("Recommended items:", results)


#WardrobeItem = {
    #"name": str,
    #"category": str,       # shirt, pants, shoes
    #"dominant_color": str, # black, blue
    #"colors": list[str],
    #"season": str,         # summer, winter, all
    #"formality": str,      # casual, semi-formal, formal
    #"sleeves": str,        # short, long, none
    #"tags": list[str]
#}
