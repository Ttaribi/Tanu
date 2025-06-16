

from flask import Flask
from flask_cors import CORS
from routes import routes

app = Flask(__name__, template_folder="templates")
app.secret_key = "replace-with-a-long-random-secret"
CORS(app, supports_credentials=True)

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

