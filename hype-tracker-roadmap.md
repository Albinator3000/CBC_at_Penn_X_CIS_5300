# Hype Tracker Agent - Tech Stack & Components

---

## Tech Stack

**Backend**
- Groq API (Llama 3.1 70B) - agent reasoning
- Flask - API server
- Python 3.10+

**Frontend**
- Vanilla JS - agent orchestration
- Chart.js - trend visualizations
- HTML/CSS - dashboard UI

**Data**
- Pre-built JSON files (Nike, Adidas, Puma, New Balance, Asics, Reebok)

---

## Components to Build

### 1. Mock Data (`data/brands.json`)
```json
{
  "nike": {
    "mentions": 15420,
    "change_pct": 23,
    "sentiment": 78,
    "avg_price": 120,
    "price_change": 8,
    "signals": ["Air Max trending", "Dunk restocks"],
    "history": [12000, 13200, 14100, 15420]
  }
}
```
**6 brands with mentions, sentiment, prices, signals, 30-day history**

### 2. Agent Core (`agent.py`)
```python
def analyze_brand(brand: str):
    # Load data from JSON
    # Call Groq with tools
    # Stream reasoning
    # Return hype score + recommendation
```
**3 tool functions:**
- `get_brand_data(brand)` → mentions, sentiment
- `calculate_hype_score(data)` → 0-100 score
- `generate_recommendation(score)` → buy/hold/sell

### 3. Flask API (`app.py`)
```python
@app.route('/analyze')
def analyze():
    brand = request.args.get('brand')
    result = agent.analyze_brand(brand)
    return jsonify(result)
```
**2 endpoints:**
- `GET /analyze?brand=nike` → single analysis
- `GET /compare?brands=nike,adidas` → head-to-head

### 4. Dashboard UI (`index.html`)
**Components:**
- Brand selector dropdown
- "Analyze" button
- Hype score gauge (0-100)
- Trend chart (Chart.js line graph)
- Sentiment meter
- Key signals list
- Recommendation card with emoji
- Agent reasoning stream (live text)

### 5. Agent Orchestrator (`static/app.js`)
```javascript
async function runAnalysis(brand) {
    // Show "thinking" animation
    // Call /analyze endpoint
    // Stream agent steps
    // Update UI components
    // Animate results
}
```

---

## File Structure

```
hype-tracker/
├── data/
│   └── brands.json           # Pre-built data for 6 brands
├── static/
│   ├── index.html            # Dashboard UI
│   ├── app.js                # Frontend orchestrator
│   └── style.css             # Dark mode styling
├── agent.py                  # Groq agent (30 lines)
├── tools.py                  # 3 tool functions (20 lines)
├── app.py                    # Flask server (15 lines)
├── .env                      # GROQ_API_KEY
└── requirements.txt
```

**Total: ~100 lines of Python, ~150 lines of JS**

---

## Build Checklist

**Backend (30 min)**
- [ ] Create brands.json with 6 brands
- [ ] Write calculate_hype_score()
- [ ] Write generate_recommendation()
- [ ] Implement Groq agent with tool calling
- [ ] Create Flask endpoints

**Frontend (30 min)**
- [ ] Build dashboard layout
- [ ] Add Chart.js for trends
- [ ] Create animated gauge
- [ ] Add brand selector
- [ ] Wire up /analyze API
- [ ] Add "thinking" animation

**Polish (15 min)**
- [ ] Dark mode styling
- [ ] Mobile responsive
- [ ] Error handling
- [ ] Loading states

**Total build time: 1-1.5 hours**

---

## Key Features

✅ **Sub-second responses** (Groq speed)  
✅ **Animated agent reasoning** (feels AI-powered)  
✅ **Visual comparisons** (Nike vs Adidas gauges)  
✅ **Portfolio ranking** (all 6 brands sorted)  
✅ **Extensible** (add features in <5 min)  
✅ **No API costs** (all mock data)

---

## Extensions to Add

**Easy additions:**
- Add more brands (expand brands.json)
- Historical backtest view
- Export analysis to PDF
- Dark/light mode toggle

**Medium additions:**
- Real Reddit API integration
- Price alerts system
- Multi-brand portfolio tracker
- Time-series predictions

**Advanced additions:**
- Real-time WebSocket updates
- Fine-tuned sentiment model
- Competitor comparison matrix
- ML-based hype prediction
