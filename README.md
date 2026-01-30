# Sneaker Hype Tracker - NLP Agent Demo
### CIS 5300: Natural Language Processing
**Guest Lecture for Prof. Chris Callison-Burch**

---

## Overview

An AI-powered sneaker brand analysis dashboard demonstrating modern NLP agent architectures. Uses **Groq's Llama 3.1 8B** with tool calling to analyze market sentiment and provide investment recommendations.

## Screenshots

### Dashboard Analysis View
![Sneaker Hype Tracker - Analysis View](screenshots/analysis-view.png)
*AI agent analyzing New Balance with hype score, recommendation, trend chart, and real-time reasoning*

### Agent Thinking State
![Agent Processing](screenshots/agent-thinking.png)
*Real-time loading state showing agent tool calling in progress*

## NLP Concepts Demonstrated

1. **Large Language Model Integration** - Llama 3.1 8B for reasoning
2. **Tool Calling & Function Execution** - LLM autonomously selects and executes tools
3. **Multi-step Agent Reasoning** - Chain-of-thought visible in real-time
4. **Natural Language to Structured Output** - Query → Analysis → Recommendation
5. **Practical Sentiment Analysis** - Market intelligence from social signals

## Tech Stack

- **Backend**: Python, Flask, Groq API
- **Agent**: Llama 3.1 8B Instant with tool calling
- **Frontend**: Vanilla JS, Chart.js
- **Data**: Mock sneaker brand metrics (8 brands)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (already configured in .env)
# GROQ_API_KEY is set

# Run server
python app.py
```

Open `http://localhost:5001` in your browser.

## Demo Flow

1. Select a sneaker brand (Nike, Adidas, Puma, etc.)
2. Click "Analyze Hype"
3. Watch the agent:
   - Call `get_brand_data()` to retrieve metrics
   - Call `calculate_hype_score()` to compute 0-100 score
   - Call `generate_recommendation()` for BUY/HOLD/SELL
   - Synthesize natural language analysis
4. View results: hype score gauge, trend chart, key signals, recommendation

## Key Features for NLP Discussion

**Agent Reasoning Transparency**
- Real-time reasoning steps displayed in UI
- Shows tool selection decisions
- Demonstrates LLM function calling

**No Hardcoded Logic**
- Agent dynamically decides tool usage
- Context-aware analysis
- Adapts reasoning to brand data

**Production-Ready**
- Sub-second response times (Groq optimization)
- Streaming responses
- Error handling

## File Structure

```
├── agent.py          # Groq agent with tool calling
├── tools.py          # 3 analysis functions
├── app.py            # Flask API server
├── data/brands.json  # Mock brand data
└── static/           # Dashboard UI
```

## Questions to Explore

- How does the agent decide which tools to call?
- What are the trade-offs of tool calling vs. end-to-end generation?
- How could we improve sentiment analysis with fine-tuning?
- What safety considerations exist for autonomous agents?

---

**Contact**: Demo for CIS 5300 NLP Course
