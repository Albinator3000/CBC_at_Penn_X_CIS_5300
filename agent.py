import os
from groq import Groq
from tools import get_brand_data, calculate_hype_score, generate_recommendation

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_brand(brand: str) -> dict:
    """Analyze sneaker brand hype using Groq agent with tool calling"""

    # Define tools for Groq
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_brand_data",
                "description": "Get current social media mentions, sentiment, and price data for a sneaker brand",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "brand": {"type": "string", "description": "Brand name (nike, adidas, puma, newbalance, asics, reebok)"}
                    },
                    "required": ["brand"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_hype_score",
                "description": "Calculate a 0-100 hype score based on brand metrics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "object", "description": "Brand data dictionary with mentions, sentiment, price info"}
                    },
                    "required": ["data"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "generate_recommendation",
                "description": "Generate buy/hold/sell recommendation based on hype score",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "score": {"type": "integer", "description": "Hype score from 0-100"}
                    },
                    "required": ["score"]
                }
            }
        }
    ]

    messages = [
        {
            "role": "system",
            "content": "You are a sneaker hype analyst. Use the provided tools to analyze brand data, calculate hype scores, and make investment recommendations. Be concise and data-driven."
        },
        {
            "role": "user",
            "content": f"Analyze the current hype level for {brand} sneakers and provide a recommendation."
        }
    ]

    reasoning_steps = []

    # Initial agent call
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=1000
    )

    # Handle tool calls
    while response.choices[0].message.tool_calls:
        tool_calls = response.choices[0].message.tool_calls
        messages.append(response.choices[0].message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = eval(tool_call.function.arguments)

            reasoning_steps.append(f"Calling {function_name} with {function_args}")

            # Execute the appropriate function
            if function_name == "get_brand_data":
                result = get_brand_data(function_args["brand"])
            elif function_name == "calculate_hype_score":
                result = calculate_hype_score(function_args["data"])
            elif function_name == "generate_recommendation":
                result = generate_recommendation(function_args["score"])

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(result)
            })

        # Continue conversation
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=1000
        )

    # Extract final analysis
    final_message = response.choices[0].message.content

    # Get final data for response
    brand_data = get_brand_data(brand)
    hype_score = calculate_hype_score(brand_data)
    recommendation = generate_recommendation(hype_score)

    return {
        "brand": brand,
        "data": brand_data,
        "hype_score": hype_score,
        "recommendation": recommendation,
        "analysis": final_message,
        "reasoning": reasoning_steps
    }
