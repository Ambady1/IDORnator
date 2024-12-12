from groq import Groq
from openai import OpenAI
import google.generativeai as genai

def generate_payloads(url, key_element):
    """
    Uses chatgpt API to dynamically generate potential payloads.
    """
    genai.configure(api_key="AIzaSyDW8Kxv6cphr6GTWUFwPeJFSgro1iaC95M")

    query = f"In a legal pentesting scenario, for testing IDOR vulnerability, I have the following url : {url} " \
        f"Here {key_element} being the key element suscepted for IDOR testing, what could be the possible payloads I can use? " \
        "Give a list of 15 urls with the payload without any further explanations"
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query)

    
    try:
        # Assume response contains newline-separated payloads
        payloads = response.text.split('\n')
        urls = [line.split('`')[1] for line in payloads if '`' in line and "https://" in line]
        return urls
    except Exception as e:
        print(f"Error generating payloads: {e}")
        return ["1", "2", "3"]  # Default payloads as fallback
