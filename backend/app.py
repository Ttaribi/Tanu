from flask import Flask
from flask_cors import CORS

from auth import auth_bp
from dashboard import dashboard_bp
from user_settings import user_settings_bp
from tanuAdmin import tanuAdmin_bp
from user_profile import user_profile_bp

app = Flask(__name__, template_folder='../frontend')
app.secret_key = '…your secret…'
CORS(app, supports_credentials=True)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(user_settings_bp)  
app.register_blueprint(tanuAdmin_bp)
app.register_blueprint(user_profile_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
