import os
import requests
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from payload import generate_payloads  # Using Groq API for payload generation
from process_Form import process_form

def send_idor(request):
    """
    Processes the form data, replaces the parameter value in the URL
    with items from dynamically generated payloads, and sends HTTP requests.
    """
    mode, url = process_form(request)
    parsed_url = urlparse(url)

    '''if not query_params:
        return [{"url": url, "payload": "N/A", "status": "Invalid URL"}]'''

    if parsed_url.query:
        query_params = parse_qs(parsed_url.query)
        key_value = list(query_params.values())[0][0]
        temp_payload = generate_payloads(url,key_value)
    else:
        key_value = os.path.basename(parsed_url.path)
        print(key_value)
        

    # Generate payloads dynamically using Groq API
    responses = []
    for payload in temp_payload:
        if parsed_url.query:
            param_key = list(query_params.keys())[0]
            query_params[param_key] = payload
            new_query = urlencode(query_params, doseq=True)
            modified_url = urlunparse(parsed_url._replace(query=new_query))

            try:
                response = requests.get(modified_url)
                responses.append({
                    "url": modified_url,
                    "payload": payload,
                    "status": response.status_code
                })
            except requests.RequestException as e:
                responses.append({
                    "url": modified_url,
                    "payload": payload,
                    "status": f"Error: {str(e)}"
                })

    return responses
