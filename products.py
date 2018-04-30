from flask_cors import CORS

from app import app

if __name__ == '__main__':
    cors = CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:8080/*"}})
    app.run()