from flask import Flask
from models import db
from routes import user_routes
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Link the db object to the app
db.init_app(app)

# Register blueprints/routes
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0",port=5000)
