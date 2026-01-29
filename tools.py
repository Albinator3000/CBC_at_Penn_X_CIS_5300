import json

def get_brand_data(brand: str) -> dict:
    """Load brand data from JSON file"""
    with open('data/brands.json', 'r') as f:
        data = json.load(f)
    return data.get(brand.lower(), {})

def calculate_hype_score(data: dict) -> int:
    """Calculate hype score (0-100) based on mentions, sentiment, and price change"""
    if not data:
        return 0

    # Weighted scoring algorithm
    mention_score = min(data.get('change_pct', 0) * 0.4, 40)
    sentiment_score = data.get('sentiment', 50) * 0.4
    price_score = min(data.get('price_change', 0) * 1.5, 20)

    total = mention_score + sentiment_score + price_score
    return max(0, min(100, int(total)))

def generate_recommendation(score: int) -> dict:
    """Generate buy/hold/sell recommendation based on hype score"""
    if score >= 75:
        return {
            "action": "BUY",
            "emoji": "🚀",
            "reason": "Strong upward momentum with high sentiment"
        }
    elif score >= 55:
        return {
            "action": "HOLD",
            "emoji": "👀",
            "reason": "Moderate hype with potential growth"
        }
    else:
        return {
            "action": "SELL",
            "emoji": "📉",
            "reason": "Declining interest and negative trends"
        }
