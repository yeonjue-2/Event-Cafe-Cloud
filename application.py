from flask import Flask
import jwt
from database import DB

app = Flask(__name__)
DB.init()

# 블루프린트
from controller import auth_controller, main_controller, user_controller

app.register_blueprint(auth_controller.bp)
app.register_blueprint(main_controller.bp)
app.register_blueprint(user_controller.bp)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5007, debug=True)
