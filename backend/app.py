from flask import Flask
from flask_cors import CORS

from auth import auth_bp
from dashboard import dashboard_bp

app = Flask(__name__, template_folder="../frontend")
app.secret_key = "…your secret…"
CORS(app, supports_credentials=True)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
