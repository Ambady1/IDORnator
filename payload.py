from groq import Groq
from process_Form import process_form


def generate_payloads(param_key):
    """
    Uses Groq API to dynamically generate potential payloads.
    """
    client = Groq(api_key="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")
    response = client.chat.completions.create(
        model="gemma-7b-it",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Given the parameter '{param_key}', identify potential encryption schemes (e.g., base64, URL encoding, hash formats) "
                    f"and create a list of test payloads for IDOR vulnerability testing. Include the following: "
                    f"1) Simple increment and decrement of numeric IDs, "
                    f"2) Variations with known encryption patterns (e.g., base64-encoded IDs), "
                    f"3) Examples of complex payloads (e.g., SQL injection-like strings or manipulated JSON structures). "
                    f"Return ONLY the payload values in a newline-separated format, with no additional explanation or details."
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
