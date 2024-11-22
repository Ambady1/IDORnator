def process_form(request):
    """
    Processes the form input and returns the mode and URL values.
    """
    mode = request.form.get("mode")
    url = request.form.get("url")
    return mode, url
