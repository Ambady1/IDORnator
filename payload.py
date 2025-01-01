import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_payloads(url, key_element):
    messages = [
        {"role": "system", "content": "You are an advanced cybersecurity expert specializing in IDOR (Insecure Direct Object Reference) vulnerability testing. Your goal is to generate precise, intelligent payload variations that test for unauthorized access to resources."},
        {"role": "user", "content": (
            "Generate a comprehensive list of IDOR test payloads with the following advanced guidelines:\n\n"
            "Payload Generation Methodology:\n"
            "1. Numeric ID Manipulation:\n"
            "   - For URLs with 'id' parameters, generate variations like:\n"
            "     a) Incrementing/decrementing IDs (id=2, id=0, id=-1)\n"
            "     b) Large/extreme numeric values (id=9999, id=1000000)\n"
            "     c) Potential admin/system IDs (id=0, id=1)\n\n"
            "2. Path/Filename Variations:\n"
            "   - Identify potential administrative or sensitive paths:\n"
            "     a) Replace user-related terms with admin variants\n"
            "     b) Explore alternative access points\n"
            "     c) Test for predictable naming conventions\n\n"
            "3. Encoding Analysis:\n"
            "   - Detect and manipulate different encoding types\n"
            "   - Generate alternative encoded payloads\n\n"
            "4. Context-Specific Payload Generation:\n"
            "   - Analyze URL structure for potential access points\n"
            "   - Generate context-aware IDOR test URLs\n\n"
            f"Specific URL to Analyze: {url}\n"
            f"Key Identifying Element: {key_element}\n\n"
            "Requirements:\n"
            "- Focus EXCLUSIVELY on IDOR vulnerability testing\n"
            "- Avoid SQL injection or other unrelated vulnerability payloads\n"
            "- Generate at least 15 unique, intelligent test URLs\n"
            "- Prioritize realistic, potentially exploitable variations\n\n"
            "Provide ONLY the generated payload URLs, one per line, without any additional explanation or commentary."
        )}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": messages[1]["content"]}]
        )

        # Extract payloads from the response
        generated_text = response.choices[0].message.content.strip()
        payloads = [line.strip() for line in generated_text.split("\n") if line.strip()]
        return payloads

    except Exception as e:
        print(f"Error generating payloads: {e}")
        return ["1", "2", "3"]  # Default payloads as fallback
    
def gen_pathtraversal(url):
    messages=[{"role": "user", "content": (
            f"In a legal pentesting scenario, for testing IDOR vulnerability, I have the following url : {url}\n"
            "Generate 15 urls with most apt payloads to bypass 403 restrictions using path traversal.\n"
            "Focus on bypassing the 403 restriction at the specified endpoint only. No need for payloads to access other server files (eg: /etc/hosts).\n"
            "Give only the urls as a list. Say nothing else, no prefixes, no suffixes - only the urls."
        )}]
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": messages[0]["content"]}]
        )

        # Extract payloads from the response
        generated_text = response.choices[0].message.content.strip()
        payloads = [line.strip() for line in generated_text.split("\n") if line.strip()]
        return payloads

    except Exception as e:
        print(f"Error generating payloads: {e}")
        return ["1", "2", "3"]  # Default payloads as fallback
    