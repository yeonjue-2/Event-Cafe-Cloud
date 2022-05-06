from flask import Flask
import jwt
import config
from database import DB

app = Flask(__name__)
DB.init()

# 블루프린트
from views import auth_views

app.register_blueprint(auth_views.bp)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
