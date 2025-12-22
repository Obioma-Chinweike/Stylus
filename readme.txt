1. Extract intents from user text
2. For each intent:
   - Filter wardrobe by formality, event, season
   - Score items using:
       - Intent confidence
       - Event match
       - Formality match
3. Merge results across intents
4. Rank and return top N
