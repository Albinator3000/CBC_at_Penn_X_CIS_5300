import os
import json
from groq import Groq
from tools import get_brand_data, calculate_hype_score, generate_recommendation

# Initialize Groq client with API key from environment
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Define tool schemas for Groq function calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_brand_data",
            "description": "Retrieve sneaker brand data including mentions, sentiment, price changes, and market signals",
            "parameters": {
                "type": "object",
                "properties": {
                    "brand": {
                        "type": "string",
                        "description": "The sneaker brand name (e.g., 'nike', 'adidas', 'puma')"
                    }
                },
                "required": ["brand"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_hype_score",
            "description": "Calculate a hype score (0-100) based on brand data object returned from get_brand_data",
            "parameters": {
                "type": "object",
                "properties": {
                    "mentions": {"type": "integer"},
                    "change_pct": {"type": "integer"},
                    "sentiment": {"type": "integer"},
                    "avg_price": {"type": "integer"},
                    "price_change": {"type": "integer"},
                    "signals": {"type": "array"},
                    "history": {"type": "array"}
                },
                "required": ["mentions", "change_pct", "sentiment", "price_change"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_recommendation",
            "description": "Generate a BUY/HOLD/SELL recommendation based on the hype score",
            "parameters": {
                "type": "object",
                "properties": {
                    "score": {
                        "type": "integer",
                        "description": "Hype score from 0-100"
                    }
                },
                "required": ["score"]
            }
        }
    }
]

def analyze_brand(brand: str) -> dict:
    """Main function to analyze brand hype and provide recommendations using Groq LLM agent"""

    # Optimized system prompt for faster processing
    system_prompt = """You are a sneaker market analyst. Analyze brands efficiently:
    1. Call get_brand_data(brand)
    2. Pass ALL returned fields to calculate_hype_score()
    3. Call generate_recommendation(score)
    4. Provide brief summary
    Use exact values from tool responses. Be concise."""

    # Initial user message
    user_message = f"Analyze the sneaker brand '{brand}' and provide a hype score and investment recommendation."

    # Initialize conversation
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    # Storage for results
    brand_data = None
    hype_score = None
    recommendation = None
    reasoning_steps = []

    # Agent loop - optimized to 6 iterations for faster processing
    for _ in range(6):
        # Call Groq API with Llama 3.1 8B (more stable for tool calling)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2,
            max_tokens=800
        )

        assistant_message = response.choices[0].message

        # Check if the model wants to call tools
        if assistant_message.tool_calls:
            # Add assistant message to conversation
            messages.append(assistant_message)

            # Process each tool call
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Log reasoning step
                reasoning_steps.append(f"Calling {function_name} with args: {function_args}")

                # Execute the appropriate function
                if function_name == "get_brand_data":
                    result = get_brand_data(function_args["brand"])
                    brand_data = result
                elif function_name == "calculate_hype_score":
                    # Pass function_args directly as the data dict
                    result = calculate_hype_score(function_args)
                    hype_score = result
                elif function_name == "generate_recommendation":
                    result = generate_recommendation(function_args["score"])
                    recommendation = result
                else:
                    result = {"error": "Unknown function"}

                # Add tool response to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(result)
                })
        else:
            # Model has finished tool calling and provided final response
            final_analysis = assistant_message.content
            break
    else:
        # If we hit max iterations
        final_analysis = "Analysis completed with available data."

    # Return structured response
    return {
        "brand": brand,
        "data": brand_data or {},
        "hype_score": hype_score or 0,
        "recommendation": recommendation or {"action": "HOLD", "emoji": "?", "reason": "Insufficient data"},
        "analysis": final_analysis,
        "reasoning": reasoning_steps
    }
