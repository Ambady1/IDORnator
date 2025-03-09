import time
import requests  # Ensure this is installed
from flask import Flask, render_template, request, stream_with_context, Response, session
from idor import send_idor
from custom_header import send_custom_header_request
from path_Traversal import path_trav
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key

@app.route("/", methods=["GET", "POST"])
def home():
    """Render the home page and handle form submission."""
    if request.method == "POST":
        mode = request.form.get("mode")

        if mode == "IDOR":
            session["idor_form_data"] = request.form.to_dict()
            return render_template("idor.html", form_data=session["idor_form_data"])
        
        elif mode == "BAC":
            session["bac_form_data"] = request.form.to_dict()
            return render_template("bac.html")

    return render_template("home.html")


@app.route("/idor-stream", methods=["GET"])
def idor_stream():
    """Stream IDOR testing results incrementally using Server-Sent Events (SSE)."""
    form_data = session.get("idor_form_data")  # Corrected key

    if not form_data:
        return Response("data: Error: No form data found.\n\n", content_type="text/event-stream")

    @stream_with_context
    def generate_results():
        flag = 0
        yield "data: Creating intelligent payloads using AI...\n\n"

        # Step 1: Test IDOR
        try:
            result1, flag = send_idor(form_data, flag)
            for entry in result1:
                analysis_result = entry.get("Result after response analysis", "")
                text_color = "text-green" if analysis_result == "VULNERABLE" else "text-red"

                yield f"data: <div class='result-item {text_color}'>" \
                      f"<p><strong>URL:</strong> {entry['url']}</p>" \
                      f"<p><strong>Payload:</strong> {entry['payload']}</p>" \
                      f"<p><strong>Status:</strong> {entry['status']}</p>" \
                      f"{f'<p><strong>Analysis:</strong> {analysis_result}</p>' if analysis_result else ''}" \
                      f"</div><hr>\n\n" 
        except Exception as e:
            yield f"data: Error in IDOR testing: {str(e)}\n\n"
            return

        # Step 2: Test Custom Headers
        if flag == 0:
            yield "data: Moving to second phase of testing...\n\n"
            time.sleep(5)
            try:
                result2, flag = send_custom_header_request(form_data, flag)
                for entry in result2:
                    analysis_result = entry.get("Result after response analysis", "")
                    text_color = "text-green" if analysis_result == "VULNERABLE" else "text-red"

                    yield f"data: <div class='result-item {text_color}'>" \
                          f"<p><strong>Header:</strong> {entry['header']}</p>" \
                          f"<p><strong>Value:</strong> {entry['value']}</p>" \
                          f"<p><strong>Status:</strong> {entry['status']}</p>" \
                          f"{f'<p><strong>Analysis:</strong> {analysis_result}</p>' if analysis_result else ''}" \
                          f"</div><hr>\n\n"
            except Exception as e:
                yield f"data: Error in custom header testing: {str(e)}\n\n"
                return

        # Step 3: Test Path Traversal
        if flag == 0:
            yield "data: Moving to third phase of testing...\n\n"
            time.sleep(5)
            try:
                result3, flag = path_trav(form_data, flag)
                for entry in result3:
                    analysis_result = entry.get("Result after response analysis", "")
                    text_color = "text-green" if analysis_result == "VULNERABLE" else "text-red"

                    yield f"data: <div class='result-item {text_color}'>" \
                          f"<p><strong>URL:</strong> {entry['url']}</p>" \
                          f"<p><strong>Status:</strong> {entry['status']}</p>" \
                          f"{f'<p><strong>Analysis:</strong> {analysis_result}</p>' if analysis_result else ''}" \
                          f"</div><hr>\n\n"
            except Exception as e:
                yield f"data: Error in path traversal testing: {str(e)}\n\n"
                return

        yield "data: Testing completed.\n\n"

    return Response(generate_results(), content_type="text/event-stream")


@app.route("/bac-stream", methods=["GET"])
def bac_stream():
    """Stream BAC testing results using SSE."""
    form_data = session.get("bac_form_data")  # Corrected key

    if not form_data:
        return Response("data: Error: No form data found.\n\n", content_type="text/event-stream")

    @stream_with_context
    def generate_results():
        yield "data: Starting BAC Testing...\n\n"

        url = form_data.get("url")
        admin_token = form_data.get("higher_token")
        user_token = form_data.get("lower_token")

        if not url or not admin_token or not user_token:
            yield "data: Error: Missing required parameters.\n\n"
            return

        headers_admin = {"Authorization": f"Bearer {admin_token}"}
        headers_user = {"Authorization": f"Bearer {user_token}"}

        try:
            # Admin Access Check
            yield "data: Checking admin access...\n\n"
            response_admin = requests.get(url, headers=headers_admin)
            admin_content = response_admin.text

            # User Access Check
            yield "data: Checking user access...\n\n"
            response_user = requests.get(url, headers=headers_user)
            user_content = response_user.text

            # Compare Responses
            if response_user.status_code == 200 and user_content == admin_content:
                yield "data: <div class='result-item text-red'>" \
                      "<p><strong>Vulnerable:</strong> User can access admin page!</p>" \
                      "</div><hr>\n\n"
            else:
                yield "data: <div class='result-item text-green'>" \
                      "<p><strong>Secure:</strong> Access restricted properly.</p>" \
                      "</div><hr>\n\n"

        except requests.RequestException as e:
            yield f"data: Error: {str(e)}\n\n"

        yield "data: BAC Testing Completed.\n\n" 

    return Response(generate_results(), content_type="text/event-stream") 


if __name__ == "__main__":
    app.run(debug=True)
