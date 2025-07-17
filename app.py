from flask import Flask
from settings import SECRET_KEY

from backend.routes.auth import auth_blueprint
from backend.routes.board import board_blueprint

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(auth_blueprint)
app.register_blueprint(board_blueprint)

if __name__ == "__main__":
    app.run(debug=True)