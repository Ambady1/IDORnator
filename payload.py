from groq import Groq
from process_Form import process_form


def generate_payloads(url,param_value):
    """
    Uses Groq API to dynamically generate potential payloads.
    """
    client = Groq(api_key="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")
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": (
                    
                    f"""
In a legal pentesting scenario, for testing IDOR vulnerability, I have the following url : '{url}'.
Here '{param_value}' being the key element suscepted for IDOR testing, what could be the possible payloads I can use? Give a list of 15 urls with the payload without any further explanations
"""

                )
            }
        ]
    )
    try:
        payloads = response.choices[0].message.content.split('\n')  # Assume response contains newline-separated payloads
        return [p.strip() for p in payloads if p.strip()]
    except Exception as e:
        print(f"Error generating payloads: {e}")
        return ["1", "2", "3"]  # Default payloads as fallback
