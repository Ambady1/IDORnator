import os
import requests
from urllib.parse import urlparse, parse_qs
from analyze_resp import resp_analyze
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

    if temp_payload[0] == '```':
        temp_payload = temp_payload[1:]

    if temp_payload[-1] == '```':
        temp_payload = temp_payload[:-1]
    
    # Generate payloads dynamically using GPT API
    responses = []
    for payload in temp_payload:
        try:
            response = requests.get(payload)
            if response.status_code == 200:
                resp_res = resp_analyze(payload, response.content)
            else:
                resp_res = None  # Set to None if no analysis is required
            
            # Create a base dictionary
            response_entry = {
                "url": payload,
                "payload": payload,
                "status": response.status_code
            }

            # Update the dictionary if resp_res indicates vulnerability
            if resp_res == 'Y':
                response_entry["Result after response analysis"] = "VULNERABLE"
                flag = 1
        
            # Append the final dictionary to responses
            responses.append(response_entry)

        except requests.RequestException as e:
            # Handle errors similarly
            responses.append({
                "url": payload,
                "payload": payload,
                "status": f"Error: {str(e)}"
            })

    return responses, flag
