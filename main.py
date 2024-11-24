from flask import Flask, render_template, request
from idor import send_idor

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Process the form and get the values
        send_idor(request)
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
