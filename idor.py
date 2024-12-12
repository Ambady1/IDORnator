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
    query_params = parse_qs(parsed_url.query)

    if not query_params:
        return [{"url": url, "payload": "N/A", "status": "Invalid URL"}]

    param_key = list(query_params.keys())[0]
   
    # Pass both the URL and the key element to generate_payloads
    temp_payload = generate_payloads(url, param_key)

    responses = []
    for payload in temp_payload:
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