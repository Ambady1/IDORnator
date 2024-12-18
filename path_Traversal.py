import requests
from payload import gen_pathtraversal
from process_Form import process_form


def path_trav(form_data,flag):
    url = process_form(form_data)

    payload = gen_pathtraversal(url)
    
    responses = []
    for payload in payload:
        try:
            response = requests.get(payload)
            responses.append({
                "url": payload,
                "status": response.status_code
            })
        except requests.RequestException as e:
            responses.append({
                "url": payload,
                "status": f"Error: {str(e)}"
            })

    return responses, flag
