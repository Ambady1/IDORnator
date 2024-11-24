import requests
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from process_Form import process_form

# Example payloads to test
temp_payload = ["1", "2", "3"]

def send_idor(request):
    """
    Processes the form data, replaces the parameter value in the URL
    with items from the temp_payload list, and sends HTTP requests.
    """
    # Extract mode and URL from the form
    mode, url = process_form(request)
    
    # Parse the URL into components
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)  # Extract query parameters

    # Identify the first parameter to replace (if any)
    if not query_params:
        # return f"Invalid URL: {url}. No query parameters found."
        print("Invalid URL")

    # Extract the first parameter and its original value
    param_key = list(query_params.keys())[0]

    # Send requests for each payload
    responses = []
    for payload in temp_payload:
        # Replace the parameter value with the payload
        query_params[param_key] = payload
        new_query = urlencode(query_params, doseq=True)
        modified_url = urlunparse(parsed_url._replace(query=new_query))

        try:
            # Send the HTTP GET request
            response = requests.get(modified_url)
            responses.append(
                f"Payload: {payload} | Status: {response.status_code} | URL: {modified_url}"
            )
        except requests.RequestException as e:
            responses.append(f"Payload: {payload} | Error: {str(e)}")

    # Return the responses as a string for debugging/logging
    # return "\n".join(responses)
    print(responses)
