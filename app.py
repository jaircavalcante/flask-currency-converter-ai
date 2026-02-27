from flask import Flask
from src.routes.ui import ui_bp

app = Flask(__name__)
app.register_blueprint(ui_bp)

if __name__ == '__main__':
    app.run(debug=True)
