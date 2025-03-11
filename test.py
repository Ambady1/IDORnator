from flask import Flask, request, jsonify

app = Flask(__name__)

ADMIN_TOKEN = "admin123"
USER_TOKEN = "user123"

@app.route('/secure-admin', methods=['GET', 'POST', 'DELETE', 'PATCH', 'PUT'])
def secure_admin():
    token = request.headers.get('Authorization')

    if not token or token != f"Bearer {ADMIN_TOKEN}":
        return jsonify({"error": "Access Denied"}), 403  # Restrict all non-admin access
    
    return jsonify({"message": f"{request.method} request successful for Admin"}), 200
# Insecure Admin Page - Broken Access Control
@app.route('/insecure-admin')
def insecure_admin():
    token = request.headers.get('Authorization')
    if token in [f"Bearer {USER_TOKEN}", f"Bearer {ADMIN_TOKEN}"]:
        return jsonify({"message": "Welcome to the Insecure Admin Page!"})
    return jsonify({"error": "Access Denied"}), 403

if __name__ == '__main__':
    app.run(debug=True, port = 8080)
