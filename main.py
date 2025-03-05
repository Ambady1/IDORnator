import time
from flask import Flask, render_template, request, stream_with_context, Response
from idor import send_idor
from custom_header import send_custom_header_request
from flask import session

from path_Traversal import path_trav

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/", methods=["GET", "POST"])
def home():
    """Render the home page and handle form submission."""
    if request.method == "POST" and request.form["mode"] == "IDOR":
        # Redirect to the idor.html page
        session["form_data"] = request.form.to_dict()
        return render_template("idor.html", form_data=request)
    elif request.method == "POST" and request.form["mode"] == "BAC":
        session["form_data"] = request.form.to_dict()
        return render_template("bac.html")
    return render_template("home.html")


@app.route("/idor-stream", methods=["GET"])
def idor_stream():
    """Stream the results incrementally using SSE."""
    form_data = session.get("form_data")
    @stream_with_context
    def generate_results():
        # Initialize the flag
        flag = 0
        # Step 1: Test IDOR
        yield "data: Creating intelligent payloads using AI...\n\n"
        result1, flag = send_idor(form_data, flag)  
        for entry in result1:
            analysis_result = entry.get("Result after response analysis", "")
            text_color = "text-green" if analysis_result == "VULNERABLE" else "text-red"

            yield (
                f"data: <div class='result-item {text_color}'>"
                f"<p><strong>URL:</strong> {entry['url']}</p>"
                f"<p><strong>Payload:</strong> {entry['payload']}</p>"
                f"<p><strong>Status:</strong> {entry['status']}</p>"
                f"{f'<p><strong>Analysis:</strong> {analysis_result}</p>' if analysis_result else ''}"
                f"</div><hr>\n\n"
            )

        # Simulate a delay and Test Custom Headers
        if flag == 0:
            yield "data: Moving to second phase of testing...\n\n"
            time.sleep(5)
            result2, flag = send_custom_header_request(form_data, flag)
            for entry in result2:
                analysis_result = entry.get("Result after response analysis", "")
                text_color = "text-green" if analysis_result == "VULNERABLE" else "text-red"

                yield (
                    f"data: <div class='result-item {text_color}'>"
                    f"<p><strong>Header:</strong> {entry['header']}</p>"
                    f"<p><strong>Value:</strong> {entry['value']}</p>"
                    f"<p><strong>Status:</strong> {entry['status']}</p>"
                    f"{f'<p><strong>Analysis:</strong> {analysis_result}</p>' if analysis_result else ''}"
                    f"</div><hr>\n\n"
                )
        
        # Simulate a delay and Test path traversal
        if flag == 0:
            yield "data: Moving to third phase of testing...\n\n"
            time.sleep(5)
            result3,flag = path_trav(form_data,flag)
            for entry in result3:
                analysis_result = entry.get("Result after response analysis", "")
                text_color = "text-green" if analysis_result == "VULNERABLE" else "text-red"
                yield (
                    f"data: <div class='result-item {text_color}'>"
                    f"<p><strong>URL:</strong> {entry['url']}</p>"
                    f"<p><strong>Status:</strong> {entry['status']}</p></div><hr>\n\n"
                    f"{f'<p><strong>Analysis:</strong> {analysis_result}</p>' if analysis_result else ''}"
                    f"</div><hr>\n\n"
                )
        # Final message
        yield "data: Testing completed.\n\n"

    return Response(generate_results(), content_type="text/event-stream")



@app.route("/bac-stream", methods=["GET"])
def bac_stream():
    """Stream the results of BAC testing."""
    form_data = session.get("form_data")

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
            yield "data: <div class='result-item text-red'>"
            yield "data: <p><strong>Vulnerable:</strong> User can access admin page!</p>"
            yield "data: </div><hr>\n\n"
        else:
            yield "data: <div class='result-item text-green'>"
            yield "data: <p><strong>Secure:</strong> Access restricted properly.</p>"
            yield "data: </div><hr>\n\n"

        yield "data: BAC Testing Completed.\n\n"

    return Response(generate_results(), content_type="text/event-stream")






if __name__ == "__main__":
    app.run(debug=True)
