import os
from dotenv import load_dotenv 
from openai import OpenAI 

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_payloads(url, key_element):
    messages = [
        {"role": "user", "content": (
            f"Generate a comprehensive list of IDOR test payloads with the URL {url} by changing the value of kay element -{key_element}.Follow these guidelines:\n\n"
            "1. If original URL contain key element with numeric parameters, generate variations like:\n"
            "     a) Incrementing/decrementing IDs  (incrementing and decrementing single unit is a mandatory case, also check random values different than that is present in original URL - {url} )\n"
            "     b) Large/extreme numeric values (id=9999, id=1000000)\n"
            "     c) Potential admin/system IDs (id=admin, id=0 etc)\n\n"
            "2. If original URL contain key element with Path/Filename Variations:\n"
            "   - For URLs with filename/path generate the values accordingly:\n"
            "     a) Replace user-related terms with admin variants\n"
            "     b) Explore alternative access points\n"
            "     c) Test for predictable naming conventions\n\n"
            "3. If original URL contain key element with some kind of encoding:\n"
            "   - Detect the encoding and generate variations accordingly\n"
            "   - Generate alternative encoded payloads\n\n"
            f"Remember the aim is to generate context-aware IDOR test URLs that most suits the {key_element}. Also avoid generating the same value that the original URL already have as the key element. Give response as a list of URLs only so that I can process it later. This is very important. Say nothing else, simply generate the URL variations as specified."
        )}
    ]

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
    
def analyze_idor(payload,resp):
    messages=[{"role": "user", "content": (
            f"In a legal pentesting scenario, for the url :  {payload} , I got the response {resp}\n"
            "Analyze the response and determine if any sensitive/user specific/PII data is exposed in the response\n"
            "Respond with letter 'Y' if any PII/sensitive/user specific data or words like 'welcome' or similar meaning as welcome exist else respond with letter 'N'. Nothing more than that needed in response"
        )}]
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": messages[0]["content"]}]
        )

        # Extract payloads from the response
        generated_resp = response.choices[0].message.content
        return generated_resp
    except Exception as e:
        print(f"Error generating payloads: {e}")
        return ["1", "2", "3"]
    
def generate_report_idor(url,payload,resp):
    messages=[{"role": "user", "content": (
            f"Write a vulnerability report based on the given data:- The original URL used for testing is this : {url}.This is the list of variation of original URL that our system marked vulnerable : {payload} and this is a list containing the html resposes we got for these URLs : {resp}.Based on the provided info generate a vulnerability report which includes heading ,description of vulnerability , steps to reproduce the vulnerability ,impact and recomendation"            
        )}]
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": messages[0]["content"]}]
        )

        # Extract payloads from the response
        generated_text = response.choices[0].message.content
        return generated_text
 
    except Exception as e:
        print(f"Error generating report: {e}")
        return ["Some Error Occured"]  # Default payloads as fallback

def generate_header_bypass_report(url,vuln_header,vuln_content):
    messages=[{"role": "user", "content": (
            f"Write a vulnerability report based on the given data:- The original URL used for testing is this : {url}. IDOR worked when the following header injection : {vuln_header} is added. The response recieved on successful IDOR is this : {vuln_content}.Based on the provided info generate a vulnerability report which includes heading ,description of vulnerability , steps to reproduce the vulnerability ,impact and recomendation"            
        )}]
    #try: