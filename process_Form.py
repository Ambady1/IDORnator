def process_form(form_data):
    """
    Processes the form input and returns the URL values.
    """
    url = form_data["url"]
    return url

def process_form_n_cookie(form_data):
    "Process url input and cookie"
    url = form_data["url"]
    session_cookie = form_data["cookie"]
    return url,session_cookie