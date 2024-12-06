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
                    
                    f"""
Given the parameter '{param_key}', analyze its structure to identify possible encoding or encryption schemes such as:
1) Base64 encoding, 
2) Hexadecimal encoding,
3) URL-safe Base64, 
4) Common hash-like patterns (e.g., MD5, SHA-256),
5) Custom obfuscation or encryption techniques.

Based on this analysis, generate a list of payloads that modify the parameter to test for IDOR vulnerabilities, including:
1) Variations of decoded and re-encoded values using the identified schemes.
2) Incremental and decremental numeric sequences within encoded formats.
3) Encoded manipulations of common test strings like SQL injection payloads, path traversal payloads, or special characters.
4) Encoded and obfuscated versions of boundary test cases, such as extreme numbers or invalid data.

Return only the payload values in a newline-separated format, with no additional explanation or details. The payloads must cover all possible edge cases for the given encoding scheme.
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
