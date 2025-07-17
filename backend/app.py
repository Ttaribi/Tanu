from flask import Flask
from flask_cors import CORS

from auth import auth_bp
from dashboard import dashboard_bp
from student_profile import student_profile_bp
from tanuAdmin import tanuAdmin_bp
app = Flask(__name__, template_folder='../frontend')
app.secret_key = '…your secret…'
CORS(app, supports_credentials=True)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(student_profile_bp)  
app.register_blueprint(tanuAdmin_bp)           

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
