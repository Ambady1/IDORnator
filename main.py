from flask import Flask, render_template, request
from process_Form import process_form

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    mode, url = None, None  # Default values
    if request.method == "POST":
        # Process the form and get the values
        mode, url = process_form(request)
    return render_template("home.html", mode=mode, url=url)

if __name__ == "__main__":
    app.run(debug=True)
