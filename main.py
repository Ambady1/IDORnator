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
    if request.method == "POST":
        # Redirect to the idor.html page
        session["form_data"] = request.form.to_dict()
        return render_template("idor.html", form_data=request)
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
            yield (
                f"data: <div class='result-item "
                f"{'text-green' if entry['status'] == 200 else 'text-red'}'>"
                f"<p><strong>URL:</strong> {entry['url']}</p>"
                f"<p><strong>Payload:</strong> {entry['payload']}</p>"
                f"<p><strong>Status:</strong> {entry['status']}</p></div><hr>\n\n"
            )

        # Simulate a delay
        yield "data: Moving to second phase of testing...\n\n"

        # Step 2: Test Custom Headers
        if flag == 0:
            result2, flag = send_custom_header_request(form_data, flag)
            for entry in result2:
                yield (
                    f"data: <div class='result-item "
                    f"{'text-green' if entry['status'] == 200 else 'text-red'}'>"
                    f"<p><strong>Header:</strong> {entry['header']}</p>"
                    f"<p><strong>Value:</strong> {entry['value']}</p>"
                    f"<p><strong>Status:</strong> {entry['status']}</p></div><hr>\n\n"
                )
        
        # Simulate a delay
        yield "data: Moving to third phase of testing...\n\n"
        
        # Step 3: Test path traversal
        if flag == 0:
            result3,flag = path_trav(form_data,flag)
            for entry in result3:
                yield (
                    f"data: <div class='result-item "
                    f"{'text-green' if entry['status'] == 200 else 'text-red'}'>"
                    f"<p><strong>URL:</strong> {entry['url']}</p>"
                    f"<p><strong>Status:</strong> {entry['status']}</p></div><hr>\n\n"
                )
            
        # Final message
        yield "data: Testing completed.\n\n"

    return Response(generate_results(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)
