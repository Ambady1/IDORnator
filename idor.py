import os
import requests
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from payload import generate_payloads  # Using Groq API for payload generation
from process_Form import process_form


def send_idor(form_data, flag):
    """
    Processes the form data, replaces the parameter value in the URL
    with items from dynamically generated payloads, and sends HTTP requests.
    """
    url = process_form(form_data)
    parsed_url = urlparse(url)

    if parsed_url.query:
        query_params = parse_qs(parsed_url.query)
        key_value = list(query_params.values())[0][0]
        temp_payload = generate_payloads(url, key_value)
    else:
        key_value = os.path.basename(parsed_url.path)
        # Ensure temp_payload is defined here
        temp_payload = generate_payloads(url, key_value)

    temp_payload = [payload.replace("```plaintext", "") for payload in temp_payload]
    
    # Generate payloads dynamically using GPT API
    responses = []
    for payload in temp_payload:
        try:
            response = requests.get(payload)
            responses.append({
                "url": payload,
                "payload": payload,
                "status": response.status_code
            })
        except requests.RequestException as e:
            responses.append({
                "url": payload,
                "payload": payload,
                "status": f"Error: {str(e)}"
            })

    return responses, flag
